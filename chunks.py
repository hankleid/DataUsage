#######################################################
#      Copyright (c) 2018 Hannah Kleidermacher.       #
#   You may use this code in any way you see fit.     #
#######################################################
import time

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
        if len(self.timestamps) > 0:
            return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(self.timestamps[0]))
    def lastTime(self):
        if len(self.timestamps) > 0:
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
    def totalTagRb(self):
        tagsRb = 0
        for tag in self.tags:
            tagsRb += tag.rb
        return tagsRb
    def totalTagTb(self):
        tagsTb = 0
        for tag in self.tags:
            tagsTb += tag.tb
        return tagsTb
    def __str__(self):
        return str(self.uid)
