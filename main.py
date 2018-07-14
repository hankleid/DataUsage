import sys
import time
import mobileDataParse
import uidNameParse

def generateNames():
    # FINDS NAME FOR EACH App IN apps
    for app in apps:
        app.name = uidNameParse.findName(sys.argv[2], app.uid)

def firstApp():
    # RETURNS App IN apps WITH FIRST LOG
    app = apps[0]
    for a in apps:
        if a.timestamps[0] < app.timestamps[0]:
            app = app.timestamps[0]
    return app

def lastApp():
    # RETURNS App IN apps WITH THE LAST LOG
    app = apps[0]
    for a in apps:
        if a.timestamps[-1] > app.timestamps[-1]:
            a = app.timestamps[-1]
    return app

def searchApps(input):
    # PASS INT
    # RETURNS App IN apps WITH UID OF 'INPUT'
    for app in apps:
        if app.uid == input:
            return app
    raise ValueError('UID not found.')

def percentage(part, whole):
    # RETURNS ROUNDED PERCENTAGE
    return round(part/whole, 1) * 100

stat = mobileDataParse.generateStat(sys.argv[1])
apps = mobileDataParse.generateApps(sys.argv[1])
mobileDataParse.generateTags(sys.argv[1], apps)
generateNames()


# PRINTS FOR USER
if len(sys.argv) == 4:
    specialApp = searchApps(int(sys.argv[3]))
    for tag in specialApp.tags:
        print("tag %s:\n*** between %s and %s:" %(tag,tag.firstTime(),tag.lastTime()))
        print("*** data tramsitted: %s" %tag.dataTransmitted())
        print("*** total data: %s\n" %tag.totalData())
else:
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
    print("UID Stats summary:\n*** between %s and %s:" %(firstApp().firstTime(),lastApp().lastTime()))
    print("*** data tramsitted: %s MB" %str(round(tb/10**6, 1)))
    print("*** total data: %s MB \n\n" %str(round(total/10**6, 1)))

    print("Xt Stats summary:\n*** between %s and %s:" %(stat.firstTime(),stat.lastTime()))
    print("*** data tramsitted: %s" %stat.dataTransmitted())
    print("*** total data: %s\n\n" %stat.totalData())

    print("\n\n\nRerun file with 3rd arg UID for detailed breakdown.")
