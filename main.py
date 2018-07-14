#######################################################
#      Copyright (c) 2018 Hannah Kleidermacher.       #
#   You may use this code in any way you see fit.     #
#######################################################
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
total = 0
tb = 0
for app in apps:
    total += (app.rb + app.tb)
    tb += app.tb

if len(sys.argv) == 4:
    specialApp = searchApps(int(sys.argv[3]))
    print("\nSUMMARY %s (uid %s):\n*** between %s and %s:" %(specialApp.name,specialApp.uid,specialApp.firstTime(),specialApp.lastTime()))
    print("*** data transmitted: %s (%s%% of total transmitted)" %(specialApp.dataTransmitted(),percentage(specialApp.tb, tb)))
    print("*** total data: %s (%s%% of total)" %(specialApp.totalData(), percentage(specialApp.rb + specialApp.tb, total)))
    print("--------------------------------------------------------------------------------\n")
    for tag in specialApp.tags:
        print("tag %s:\n*** between %s and %s:" %(tag,tag.firstTime(),tag.lastTime()))
        print("*** data transmitted: %s (%s%% of total transmitted)" %(tag.dataTransmitted(),percentage(tag.tb, tb)))
        print("*** total data: %s (%s%% of total)\n" %(tag.totalData(),percentage(tag.rb + tag.tb, total)))
else:
    print("\nUID Stats SUMMARY:\n*** between %s and %s:" %(firstApp().firstTime(),lastApp().lastTime()))
    print("*** data transmitted: %s MB" %str(round(tb/10**6, 1)))
    print("*** total data: %s MB\n" %str(round(total/10**6, 1)))

    print("Xt Stats SUMMARY:\n*** between %s and %s:" %(stat.firstTime(),stat.lastTime()))
    print("*** data transmitted: %s" %stat.dataTransmitted())
    print("*** total data: %s" %stat.totalData())
    print("--------------------------------------------------------------------------------\n")

    for app in apps:
        print("\n%s:" %app.name)
        print("****** user ID %s: %s (%s%% of total); %s (%s%% of transmitted)" %(app.uid,app.totalData(),str(percentage(app.rb + app.tb, total)),app.dataTransmitted(),str(percentage(app.tb, tb))))
        for tag in app.tags:
            print("tag %s: %s (%s%% of total); %s (%s%% of transmitted)" %(tag,tag.totalData(),percentage(tag.rb + tag.tb, total),tag.dataTransmitted(),percentage(tag.tb, tb)))

    print("\n\nRerun file with 4th arg UID for detailed breakdown.")
