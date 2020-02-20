# GarConSwim

A python script that converts swimming splits, as exported from Garmin Connect, to readable text.

## Usage

Open **Garmin Connect** and browse the activities until you locate the swimming activity of your interest. Note that this has to be a lap swimming, i.e., at the pool.

The click the gear and select "export splits to csv". You will obtain a file called `activity_xxxxxxx.csv`, with a format similar to the following:

```
"","Intervals","Swim Stroke","Lengths","Distance","Time","Cumulative Time","Avg Pace","Best Pace","Avg. Swolf","Avg HR","Max HR","Total Strokes","Avg Strokes","Calories"
"","1","Drill","4","100","3:22,6","3:22,6","0","0","0","--","--","0","0","--
        
    "
"","","Drill","--","25,00","0:50,7","0:50,7","0","0","--","--","--","0","--","7
        
    "
"","","Drill","--","25,00","0:50,7","1:41,3","0","0","--","--","--","0","--","7
        
    "
"","","Drill","--","25,00","0:50,7","2:32,0","0","0","--","--","--","0","--","7
        
    "
"","","Drill","--","25,00","0:50,7","3:22,6","0","0","--","--","--","0","--","7
        
    "
"","","Rest","0","0","0:24,6","3:47,2","0","0","0","--","--","0","0","0
        
    "
"","2","Freestyle","8","200","3:23,5","7:10,6","1:42","1:32","36","--","--","82","10","48
        
    "
(More...)
```
You can open this with **Gnumeric**, *LibreOffice's* **Calc**, *MS Office's* **Excel** and many other similar spreadsheets. But if you apply *garconswim* to that file instead, you will get a readable report in text form, like the following one: 

```
$ ./garconswim.py activity_4568255587.csv
4200m  1:23:19 1:43/100m SWOLF:37 (best: 1:20/100m) AvgStrokes: 11
    #1 100m drill 3:22,6
    #2 200m freestyle 3:23,5
        1:42/100m SWOLF:36 (best: 1:32/100m) AvgStrokes: 10
    #3 300m freestyle 5:13,2
        1:44/100m SWOLF:37 (best: 1:40/100m) AvgStrokes: 11
    #4 400m freestyle 7:30,4
        1:53/100m SWOLF:40 (best: 1:35/100m) AvgStrokes: 12
    #5 400m mixed 8:09,0
        2:02/100m SWOLF:42 (best: 1:37/100m) AvgStrokes: 11
    #6 300m drill 6:33,9
    #7 300m freestyle 5:21,2
        1:47/100m SWOLF:38 (best: 1:44/100m) AvgStrokes: 11
    #8 2000m freestyle 30:05
        1:30/100m SWOLF:33 (best: 1:20/100m) AvgStrokes: 11
    #9 200m mixed 5:44,0
        2:52/100m SWOLF:60 (best: 2:26/100m) AvgStrokes: 17
```

## Caveats

1. **GarConSwim** is a script written in **Python 3** (remember that Python 2 is not totally deprecated). It specifies `python 3`in its shebang. If you need cannot specify it to be executed with **Python 3**, you can invoke it this way:

```
$ python garconswim.py activity_4568255587.csv
```

Or edit the first commented line of the script (the *shebang*), changing `/usr/bin/env python3` for `/usr/bin/python`.

2. This script is valid for swimming activities at the pool, but won't work with other activities like hiking, for example, since the CSV file contains other different fields.
