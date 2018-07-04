#############################
## by Hannah Kleidermacher ##
##       3 July 2018       ##
#############################

import sys
import time
fileName = sys.argv[1]
file = open(fileName, 'r')
lines = file.readlines()

class Stat:
    rb = 0
    tb = 0
    timestamps = []

    def addRb(self, amt):
        self.rb += amt
    def addTb(self, amt):
        self.tb += amt
    def addTime(self, time):
        self.timestamps.append(time)
    def firstTime(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(self.timestamps[0]))
    def lastTime(self):
        return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(self.timestamps[-1]))
    def dataReceived(self):
        return str(float(self.rb) / 10**6) + " MB"
    def dataTransmitted(self):
        return str(float(self.tb) / 10**6) + " MB"
    def totalData(self):
        return str((float(self.rb + self.tb)) / 10**6) + " MB"

class App(Stat):
    uid = 0
    tag = 0x0

    def __init__(self, u, t):
        self.uid = u
        self.tag = t

stat = Stat()
apps = []

def scanDataChunk(thing, s):
    # PASS Stat OR App; STRING TO BE SCANNED
    # PROCESSES rb, tb, AND timestamps

    thing.addRb(int(s[s.find('rb')+3:s.find('rp')-1]))
    thing.addTb(int(s[s.find('tb')+3:s.find('tp')-1]))
    thing.addTime(int(s[s.find('st')+3:s.find('rb')-1]))

def generateStat():
    inXt = False
    xtMetered = False
    readingData = False

    for line in lines:
        if 'Xt stats' in line:
            inXt = True
        if inXt and ('MOBILE' and 'metered=true') in line:
            xtMetered = True
        if xtMetered and 'st=' in line:
            readingData = True
            scanDataChunk(stat, line)
        if readingData and 'st=' not in line:
            break

def grabUID(s):
    return int(s[s.find('uid')+4:s.find('set')-1])

def grabTag(s):
    return hex(int(s[s.find('tag')+4:s.find('\n')], 16))

def existingApp(a):
    # PASS App
    # CHECKS IF APP HAS ALREADY BEEN RECORDED
    for app in apps:
        if a.uid == app.uid and a.tag == app.tag:
            return app
    return None

def generateApps():
    inUIDTag = False
    infoGrabbed = False

    for line in lines:
        if 'UID tag stats' in line:
            inUIDTag = True
        if inUIDTag and ('uid=' and 'tag=') in line:
            currentA = App(grabUID(line), grabTag(line))
            infoGrabbed = True
            if existingApp(currentA) is None:
                apps.append(currentA)
            else:
                currentA = existingApp(currentA)
        if infoGrabbed and 'st=' in line:
            scanDataChunk(currentA, line)
        if infoGrabbed and 'type=WIFI' in line:
            break

generateApps()
for app in apps:
    print(str(app.rb) + " " + str(app.tb))
'''print("\n*** between " + stat.firstTime() + " and " + stat.lastTime() + ":")
print("***\n*** data received: " + stat.dataReceived())
print("*** data tramsitted: " + stat.dataTransmitted())
print("*** total data: " + stat.totalData() + "\n")'''
