#!/usr/bin/env python3

# Convert (c) Baltasar 2019 MIT License <baltasarq@gmail.com>
# ConveRT Converts training from Garmin CSV format to a readable text format.


import csv
import argparse


class Split:
    """Holds the info about a given split time."""
    def __init__(self, n, stroke, d, t, avg, best, swolf, avg_strokes):        
        self._num = str(n).strip()
        self._stroke = stroke.strip().lower()
        self._distance = Split.convert_distance(d)
        self._time = str(t).strip()
        self._avg_pace = str(avg).strip() if avg != "--" else ""
        self._best_pace = str(best).strip() if best != "--" else ""
        self._swolf = int(float(swolf)) if swolf else ""
        self._avg_strokes = int(float(avg_strokes)) if avg_strokes else ""
        self._rest_time = ""
        
    @staticmethod
    def convert_distance(d):
        toret = -1
        
        d = d.strip()
        if d:
            d = d.replace('.', "")
            toret = int(float(d))
        
        return toret
    
    @property
    def num(self):
        return self._num
    
    @property
    def stroke_style(self):
        return self._stroke

    @property
    def distance(self):
        return self._distance
    
    @property
    def time(self):
        return self._time
    
    @property
    def avg_pace(self):
        return self._avg_pace
    
    @property
    def best_pace(self):
        return self._best_pace
    
    @property
    def swolf(self):
        return self._swolf
    
    @property
    def avg_strokes(self):
        return self._avg_strokes
    
    @property
    def rest_time(self):
        return self._rest_time
    
    def set_rest(self, rest_time):
        self._rest_time = rest_time
        
    @property
    def is_summary(self):
        num = str(self.num).strip().lower()
        return num == "summary"
    
    def __str__(self):
        toret = ""
        
        if not self.is_summary:
           toret += "    #" + self.num + ' '
            
        toret += str.format("{}m {} {}",
                          self.distance,
                          self.stroke_style,
                          self.time)
        
        avg_pace = str(self.avg_pace).strip()
        if len(avg_pace) > 0 and avg_pace != "0":
            if not self.is_summary:
                toret += "\n\t"
            else:
                toret += ' '
            toret += avg_pace + "/100m"
        
        swolf = str(self.swolf).strip()
        if len(swolf) > 0 and swolf != "0":
            toret += " SWOLF:" + swolf
        
        best_pace = str(self.best_pace).strip()
        if (len(best_pace) > 0
        and best_pace != "0"
        and best_pace != "0:"):
            toret += str.format(" (best: {}/100m)", best_pace)

        if self.avg_strokes and int(self.avg_strokes) > 0:
            toret += " AvgStrokes: " + str(self.avg_strokes)
            
        if len(self.rest_time) > 0:
            toret += " d(" + str(self.rest_time) + ')'
            
        return toret + "\n"


class Splits:
    COL_INTERVALS = "Intervals"
    COL_SWIM_STROKE = "Swim Stroke"
    COL_DISTANCE = "Distance"
    COL_TIME = "Time"
    COL_PACE = "Avg Pace"
    COL_BEST_PACE = "Best Pace"
    COL_SWOLF = "Avg. Swolf"
    COL_STROKES = "Avg Strokes"
    
    
    """Holds all splits"""
    def __init__(self, nf):
        self._file_name = nf
        self._splits = []
        self._summary = None
        
    @property
    def file_name(self):
        return self._file_name
    
    @property
    def summary(self):
        toret = self._summary
        
        if toret == None:
            toret = self.calculate_summary()
            
        return toret
    
    def set_summary(self, summary_split):
        self._summary = summary_split
    
    def read(self):
        """Reads all the splits in the file."""
        i = -1
        try:
            with open(self._file_name, newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=',')
                
                # Split, stroke, lengths, d, t, avg, best, swolf
                # Avg HR, Max HR, Total Strokes, Avg Strokes, Calories
                for row in reader:
                    i += 1
                    
                    if (not row[Splits.COL_INTERVALS]
                    or '.' in row[Splits.COL_INTERVALS]):
                        continue            # Discard splits per length
                    
                    # Put the "resting time" in the previous split
                    if row[Splits.COL_SWIM_STROKE].strip().lower() == "rest":
                        rest_time = row[Splits.COL_TIME]
                        if len(self._splits) > 0:
                            self._splits[-1].set_rest(rest_time)
                        continue
                    
                    avg_strokes = row[Splits.COL_STROKES]
                    if (not avg_strokes
                        or avg_strokes == "--"):
                        avg_strokes = 0
                                       
                    split = Split(row[Splits.COL_INTERVALS],    # num
                                  row[Splits.COL_SWIM_STROKE],  # stroke style
                                  row[Splits.COL_DISTANCE],     # distance
                                  row[Splits.COL_TIME],         # time
                                  row[Splits.COL_PACE],         # avg
                                  row[Splits.COL_BEST_PACE],    # best
                                  row[Splits.COL_SWOLF],        # swolf
                                  avg_strokes)
                                        
                    if split.is_summary:
                        self.set_summary(split)
                    else:
                        self._splits.append(split)
                        
        except ValueError as exc:
            print("Could not read field at row ", i, ":\n\t", str(exc),
                  file=sys.stderr)
        except UnicodeDecodeError as exc:
            print("Bad encoding, convert to UTF-8:\n\t" + str(exc),
                  file=sys.stderr)
            
    def calculate_summary(self):
        distance = 0
        for split in self._splits:
            distance += int(float(split.distance))
            
        return Split("Summary", "", str(distance), "", "", "", "", "")
    
    def __str__(self):
        toret = str(self.summary)
        return toret + "".join([str(x) for x in self._splits])


def prepareArgParser():
    """Prepares the argument parser.
        :return: An argparse.ArgumentParser.
    """
    parser = argparse.ArgumentParser(
                description="Creates a readable version of \
                swimming training partials in Garmin's CSV:\n\n")
    parser.add_argument("input_file",
                        type=str, help="The input file in CSV format.")

    return parser


if __name__ == "__main__":
    parser = prepareArgParser()
    args = parser.parse_args()
    nf = args.input_file
    
    splits = Splits(nf)
    splits.read()
    print(splits)
