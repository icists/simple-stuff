#!/usr/bin/python

'''Auto-name filler

Takes names from CSV file and automatically fills then in form in correct
position. Created to reduce load of participant-management tf. 

Assumes that program run in full-screen mode'''

import pywinauto, time

START_COOR = (150, 230)
HOR_DIFF = 272
VER_DIFF = 38*5
HOR_NUM = 7
VER_NUM	= 6
ATTR_NUM = 3
ATTR_YDIFF = [38, 38, 38]
TIME_INTERVAL = 0.05 # when program can't follow the fast inputs

class Participant(object):
    def __init__(self, first, last, attrs):
	assert len(attrs) == ATTR_NUM
	self._name = first + '{SPACE}' + last
	self._attrs = attrs
	
    def getName(self):
	return self._name
    
    def getAttrs(self, num):
	return self._attrs[num]

def waitFor(name):
    '''returns window handler for name'''
    app = pywinauto.application.Application()
    ex = False
    while not ex:
	try:
	    boom = app.window_(title_re = ".*"+name+".*")
	    ex = True
	except pywinauto.findbestmatch.MatchError:
	    time.sleep(1)
    time.sleep(2)
    return boom

def getNames(csv_filepath):
    '''reads names from csv file, returns list of names'''
    f = open(csv_filepath)
    names = []
    for line in f:
	all_attrs = line.strip().split(',')
	first, last, attrs = all_attrs[0], all_attrs[1], all_attrs[2:]
	p = Participant(first, last, attrs)
	names.append(p)
    f.close()
    return names

def unitCheck(prog_name):
    hndlr = waitFor(prog_name)
    work_coor = list(START_COOR)
    for y in xrange(VER_NUM):
	for x in xrange(HOR_NUM):
	    work_coor = [START_COOR[0] + x*HOR_DIFF,START_COOR[1] + y*VER_DIFF]
	    hndlr.ClickInput( coords = work_coor )
	    hndlr.TypeKeys('a')
	    time.sleep(0.05)
	    hndlr.TypeKeys('\b')

def attrCheck(prog_name):
    hndlr = waitFor(prog_name)
    work_coor = list(START_COOR)
    hndlr.ClickInput( coords = work_coor )
    hndlr.TypeKeys('a')
    time.sleep(0.05)
    hndlr.TypeKeys('\b')
    for i in xrange(ATTR_NUM):
	work_coor[1] += ATTR_YDIFF[i]
	hndlr.ClickInput( coords = work_coor )
	hndlr.TypeKeys('a')
	time.sleep(0.05)
	hndlr.TypeKeys('\b')

def worker(prog_name, names):
    hndlr = waitFor(prog_name)
    work_coor = list(START_COOR)
    for y in xrange(VER_NUM):
	for x in xrange(HOR_NUM):
	    work_coor = [START_COOR[0] + x*HOR_DIFF,START_COOR[1] + y*VER_DIFF]
	    time.sleep(TIME_INTERVAL)
	    hndlr.ClickInput( coords = work_coor )
	    try:
		p = names[0]
	    except:
		return
	    hndlr.TypeKeys(p.getName())
	    for i in xrange(ATTR_NUM):
		work_coor[1] += ATTR_YDIFF[i]
		time.sleep(TIME_INTERVAL)
		hndlr.ClickInput( coords = work_coor )
		hndlr.TypeKeys(p.getAttrs(i))
	    del names[0]
		
names = getNames('OCs.csv')
worker('Book1 - Excel', names)