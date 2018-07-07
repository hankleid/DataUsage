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
    def __init__(self):
        self.rb = 0
        self.tb = 0
        self.timestamps = []
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

class Tag(Stat):
    def __init__(self, t):
        super().__init__()
        self.tag = t
    def __str__(self):
        return str(self.tag)

class App(Stat):
    def __init__(self, u):
        super().__init__(self)
        self.uid = u
        self.tags = []
    def addTag(self, Tag):
        self.tags.append(Tag)
    def totalTagData(self):
        tagData = 0
        for tag in self.tags:
            tagData += tag.tb + tag.rb
        return tagData

stat = Stat()
apps = []

def scanDataChunk(thing, s):
    # PASS ANY KIND OF Stat; STRING TO BE SCANNED
    # PROCESSES rb, tb, AND timestamps

    thing.addRb(int(s[s.find('rb')+3:s.find('rp')-1]))
    thing.addTb(int(s[s.find('tb')+3:s.find('tp')-1]))
    thing.addTime(int(s[s.find('st')+3:s.find('rb')-1]))

def generateStat():
    inXtStats = False
    xtMetered = False
    readingData = False

    for line in lines:
        if 'Xt stats' in line:
            inXtStats = True
        if inXtStats and ('MOBILE' and 'metered=true') in line:
            xtMetered = True
        if xtMetered and 'st=' in line:
            readingData = True
            scanDataChunk(stat, line)
        if readingData and 'st=' not in line:
            break

def grabUID(s):
    return int(s[s.find('uid')+4:s.find('set')-1])

def grabTag(s):
    return s[s.find('tag')+4:s.find('\n')]

def existingApp(a):
    for app in apps:
        if app.uid == a.uid:
            return app
    return None

def existingTag(a, t):
    # PASS App
    # CHECKS IF App's CERTAIN Tag HAS ALREADY BEEN RECORDED
    for tag in a.tags:
        if tag.tag == t.tag:
            return tag
    return None

def removeEmptyApps():
    for app in reversed(apps):
        if app.rb + app.tb == 0:
            apps.remove(app)

def generateApps():
    inUIDStats = False
    uidMetered = False
    infoGrabbed = False

    for line in lines:
        if 'UID stats' in line:
            inUIDStats = True
        if inUIDStats and ('MOBILE' and 'metered=true' and 'uid=') in line:
            uidMetered = True
            currentUID = grabUID(line)
            a = App(currentUID)
            infoGrabbed = True

            if existingApp(a) is None:
                apps.append(a)
            else:
                a = existingApp(a)
        if uidMetered and 'st=' in line:
            scanDataChunk(a, line)
        if infoGrabbed and 'type=WIFI' in line:
            break

def generateTags():
    inUIDTag = False
    infoGrabbed = False

    for line in lines:
        if 'UID tag stats' in line:
            inUIDTag = True
        if inUIDTag and ('uid=' and 'tag=') in line:
            currentTag = Tag(grabTag(line))
            a = existingApp(App(grabUID(line)))
            infoGrabbed = True

            if existingTag(a, currentTag) is None:
                a.addTag(currentTag)
            else:
                currentTag = existingTag(a, currentTag)
        if infoGrabbed and 'st=' in line:
            scanDataChunk(currentTag, line)
        if infoGrabbed and 'type=WIFI' in line:
            break

    for app in apps:
        diff = app.tb + app.rb - app.totalTagData()
        t = Tag("Untagged")
        t.addRb(diff)
        app.addTag(t)


generateStat()
generateApps()
generateTags()
removeEmptyApps()

total = 0
for app in apps:
    total += (app.rb + app.tb)
    print("****** user ID " + str(app.uid) + ": " + app.totalData())
    for tag in app.tags:
        print("tag " + str(tag) + ": " + tag.totalData())

    print()
print(total)

print("\n*** between " + stat.firstTime() + " and " + stat.lastTime() + ":")
print("***\n*** data received: " + stat.dataReceived())
print("*** data tramsitted: " + stat.dataTransmitted())
print("*** total data: " + stat.totalData() + "\n\n")
