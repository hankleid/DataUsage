#############################
## by Hannah Kleidermacher ##
##       3 July 2018       ##
#############################
import time
import chunks

def scanDataChunk(thing, s):
    # PASS ANY KIND OF Stat; STRING TO BE SCANNED
    # PROCESSES rb, tb, AND timestamps

    thing.addRb(int(s[s.find('rb')+3:s.find('rp')-1]))
    thing.addTb(int(s[s.find('tb')+3:s.find('tp')-1]))
    thing.addTime(int(s[s.find('st')+3:s.find('rb')-1]))

def generateStat(fn):
    # SCANS FILE FOR Xt STATS
    file = open(fn, 'r')
    lines = file.readlines()

    stat = chunks.Stat()
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
    return stat

def grabUID(s):
    # RETURNS THE INT UID IN STR s
    return int(s[s.find('uid')+4:s.find('set')-1])

def grabTag(s):
    # RETURNS THE STR TAG IN STR s
    return s[s.find('tag')+4:s.find('\n')]

def existingApp(a, apps):
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

def removeEmptyApps(apps):
    # REMOVES EMPTY (ESSENTIALLY NO DATA) Apps IN apps
    for app in reversed(apps):
        if round((app.rb + app.tb)/10**6,1) == 0.0:
            apps.remove(app)
        for tag in reversed(app.tags):
            if round((tag.rb + tag.tb)/10**6,1) == 0.0:
                app.tags.remove(tag)

def generateApps(fn):
    # SCANS FILE FOR UIDS; ADDS AppS TO apps ACCORDINGLY
    # RETURNS LIST OF AppS
    file = open(fn, 'r')
    lines = file.readlines()

    apps = []
    inUIDStats = False
    uidMetered = False
    infoGrabbed = False

    for line in lines:
        if 'UID stats' in line:
            inUIDStats = True
        if inUIDStats and ('MOBILE' and 'metered=true' and 'uid=') in line:
            uidMetered = True
            currentUID = grabUID(line)
            a = chunks.App(currentUID)
            infoGrabbed = True

            if existingApp(a, apps) is None:
                apps.append(a)
            else:
                a = existingApp(a, apps)
        if uidMetered and 'st=' in line:
            scanDataChunk(a, line)
        if infoGrabbed and 'type=WIFI' in line:
            break
    return apps

def generateTags(fn, apps):
    # SCANS FILE FOR TAGS; ADDS TAGS TO EACH apps App ACCORDINGLY
    file = open(fn, 'r')
    lines = file.readlines()

    inUIDTag = False
    infoGrabbed = False

    for line in lines:
        if 'UID tag stats' in line:
            inUIDTag = True
        if inUIDTag and ('uid=' and 'tag=') in line:
            currentTag = chunks.Tag(grabTag(line))
            a = existingApp(chunks.App(grabUID(line)), apps)
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
        diff = app.tb - app.totalTagTb()
        t = chunks.Tag("Untagged")
        t.addTb(diff)
        diff = app.rb - app.totalTagRb()
        t.addRb(diff)
        app.addTag(t)
    removeEmptyApps(apps)
