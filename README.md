# DataUsage
#### Copyright (c) 2018 Hannah Kleidermacher. You may use this code in any way you see fit.


adb shell dumpsys package  > packages.out
adb shell dumpsys netstats detail full > usage.out
python3 main.py usage.out packages.out 


--------------------------------------------------
argv[0] (directory): this repo's mobileDataParse.py

argv[1] (directory): data file w/ Xt stats, UID stats, UID tag stats

argv[2] (directory): data file w/ package names

argv[3]* (int): UID, for app breakdown

```
$python argv[0] argv[1] argv[2] (argv[3])
```
*optional
