#############################
## by Hannah Kleidermacher ##
##       3 July 2018       ##
#############################

import sys
import time
fileName = sys.argv[1]
file = open(fileName, 'r')
lines = file.readlines()

inXt = False
xtMetered = False
readingData = False
rb = 0
tb = 0
timestamps = []

for line in lines:
    if 'Xt stats' in line:
        inXt = True
    if inXt and ('MOBILE' and 'metered=true') in line:
        xtMetered = True
    if xtMetered and 'st=' in line:
        readingData = True
        #print(line) for testing
        # FIND rb AND tb WITHIN THE LINE & ADD RESPECTIVELY
        rb += int(line[line.index('rb')+3:line.index('rp')-1])
        tb += int(line[line.index('tb')+3:line.index('tp')-1])
        # ADD TIME TO LIST OF TIMES
        timestamps.append(int(line[line.index('st')+3:line.index('rb')-1]))
    if readingData and 'st=' not in line:
        break

def dataReceived():
    return str(float(rb) / 10**6) + " MB"
def dataTransmitted():
    return str(float(tb) / 10**6) + " MB"
def totalData():
    return str((float(rb + tb)) / 10**6) + " MB"
def firstTime():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(timestamps[0]))
def lastTime():
    return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(timestamps[-1]))

print("\n*** between " + firstTime() + " and " + lastTime() + ":")
print("***\n*** data received: " + dataReceived())
print("*** data tramsitted: " + dataTransmitted())
print("*** total data: " + totalData() + "\n")
