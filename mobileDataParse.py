#############################
## by Hannah Kleidermacher ##
##       3 July 2018       ##
#############################

import sys
import time
import uidNameParse
fileName = sys.argv[1]
file = open(fileName, 'r')
lines = file.readlines()

class Stat:
    # HAS rb (RECEIVED DATA), tb (TRANSMITTED DATA), timestamps (LIST OF ALL TIMES IN ORDER)
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
        return str(round(self.rb/10**6, 1)) + " MB"
    def dataTransmitted(self):
        return str(round(self.tb/10**6, 1)) + " MB"
    def totalData(self):
        return str(round((self.rb + self.tb)/10**6, 1)) + " MB"

class Tag(Stat):
    # A Stat WITH A tag STR
    def __init__(self, t):
        super().__init__()
        self.tag = t
    def __str__(self):
        return str(self.tag)

class App(Stat):
    # A Stat WITH A uid INT, LIST OF tagS, AND name STR
    def __init__(self, u):
        super().__init__()
        self.uid = u
        self.name = ''
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
    # SCANS FILE FOR Xt STATS
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
    # RETURNS THE INT UID IN STR s
    return int(s[s.find('uid')+4:s.find('set')-1])

def grabTag(s):
    # RETURNS THE STR TAG IN STR s
    return s[s.find('tag')+4:s.find('\n')]

def existingApp(a):
    # PASS App
    # RETURNS app IF a AND app SHARE A UID
    for app in apps:
        if app.uid == a.uid:
            return app
    return None

def existingTag(a, t):
    # PASS App
    # CHECKS IF a'S CERTAIN tag HAS ALREADY BEEN RECORDED
    for tag in a.tags:
        if tag.tag == t.tag:
            return tag
    return None

def generateApps():
    # SCANS FILE FOR UIDS; ADDS AppS TO apps ACCORDINGLY
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
    # SCANS FILE FOR TAGS; ADDS TAGS TO EACH apps App ACCORDINGLY
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

def generateNames():
    # FINDS NAME FOR EACH App IN apps
    for app in apps:
        app.name = uidNameParse.findName(sys.argv[2], app.uid)

def removeEmptyApps():
    # REMOVES EMPTY (NO DATA) Apps IN apps
    for app in reversed(apps):
        if app.rb + app.tb == 0:
            apps.remove(app)

def firstApp():
    # RETURNS App IN apps WITH FIRST LOG
    a = apps[0]
    for app in apps:
        if a.timestamps[0] > app.timestamps[0]:
            a = app.timestamps[0]
    return a

def lastApp():
    # RETURNS App IN apps WITH THE LAST LOG
    a = apps[0]
    for app in apps:
        if a.timestamps[-1] < app.timestamps[-1]:
            a = app.timestamps[-1]
    return a

def percentage(part, whole):
    # RETURNS ROUNDED PERCENTAGE
    return round(part/whole, 1) * 100

generateStat()
generateApps()
generateTags()
removeEmptyApps()
generateNames()

# PRINTS FOR USER
total = 0
tb = 0
for app in apps:
    total += (app.rb + app.tb)
    tb += app.tb
for app in apps:
    print(str(app.name) + ":")
    print("****** user ID " + str(app.uid) + ": " + app.totalData() + " (" + str(percentage(app.rb + app.tb, total)) + "%" + " of total); " + app.dataTransmitted() + " (" + str(percentage(app.tb, tb)) + "%" + " of transmitted)")
    for tag in app.tags:
        print("tag " + str(tag) + ": " + tag.totalData() + " (" + str(percentage(tag.rb + tag.tb, total)) + "%" + " of total); " + tag.dataTransmitted() + " (" + str(percentage(tag.tb, tb)) + "%" + " of transmitted)")

    print()

print("\n\n\n")
print("UID Stats summary:\n*** between " + firstApp().firstTime() + " and " + lastApp().lastTime() + ":")
print("*** data tramsitted: " + str(round(tb/10**6, 1)) + " MB")
print("*** total data: " + str(round(total/10**6, 1)) + " MB" + "\n\n")

print("Xt Stats summary:\n*** between " + stat.firstTime() + " and " + stat.lastTime() + ":")
print("*** data tramsitted: " + stat.dataTransmitted())
print("*** total data: " + stat.totalData() + "\n\n")

#print("\n\n\nRerun file with 3rd arg UID for detailed breakdown.")
