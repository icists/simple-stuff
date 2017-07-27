#!/usr/bin/python

'''Auto-name filler

Takes names from CSV file and automatically fills then in form in correct
position. Created to reduce load of participant-management tf. 

Assumes that program run in full-screen mode'''

import pywinauto, time

START_COOR = (150, 230)
HOR_DIFF = 272
VER_DIFF = 38
HOR_NUM = 7
VER_NUM	= 6
ATTR_NUM = 2
ATTR_XDIFF = [5, 4]
ATTR_YDIFF = [38, 38]
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
	first, last, attrs = all_attrs[0], all_attrs[1], all_attrs[2:2+ATTR_NUM]
	p = Participant(first, last, attrs)
	names.append(p)
    f.close()
    return names

def unitCheck(prog_name):
    '''Checks HOR_DIFF, VER_DIFF coordinates by typing a test 'a'
    Does not check attribute coordinates'''
    hndlr = waitFor(prog_name)
    work_coor = list(START_COOR)
    for y in xrange(VER_NUM):
	for x in xrange(HOR_NUM):
	    work_coor = [START_COOR[0] + int(x*HOR_DIFF),
                         START_COOR[1] + int(y*VER_DIFF)]
	    hndlr.ClickInput( coords = work_coor )
	    hndlr.TypeKeys('a')
	    time.sleep(0.05)
	    hndlr.TypeKeys('\b')

def attrCheck(prog_name):
    '''Checks ATTR_XDIFF, ATTR_YDIFF coordinates by typing test 'a'
    Does not check HOR_DIFF, VER_DIFF'''
    hndlr = waitFor(prog_name)
    work_coor = list(START_COOR)
    hndlr.ClickInput( coords = work_coor )
    hndlr.TypeKeys('a')
    time.sleep(0.05)
    hndlr.TypeKeys('\b')
    for i in xrange(ATTR_NUM):
        work_coor[0] += ATTR_XDIFF[i]
	work_coor[1] += ATTR_YDIFF[i]
	hndlr.ClickInput( coords = work_coor )
	hndlr.TypeKeys('a')
	time.sleep(0.05)
	hndlr.TypeKeys('\b')

def worker(prog_name, names):
    '''Inputs name information to program you are using. 
    ::Parameters::
    prog_name: the window name of the program (e.g., "Book1 - Excel")
    names: a list of Participant instances'''
    hndlr = waitFor(prog_name)
    work_coor = list(START_COOR)
    for y in xrange(VER_NUM):
	for x in xrange(HOR_NUM):
	    work_coor = [START_COOR[0] + int(x*HOR_DIFF),
                         START_COOR[1] + int(y*VER_DIFF)]
	    time.sleep(TIME_INTERVAL)
	    hndlr.ClickInput(coords = work_coor)
	    try:
		p = names[0]
	    except:
		return
	    hndlr.TypeKeys(p.getName())
	    for i in xrange(ATTR_NUM):
                work_coor[0] += ATTR_XDIFF[i]
		work_coor[1] += ATTR_YDIFF[i]
		time.sleep(TIME_INTERVAL)
		hndlr.ClickInput(coords = work_coor)
		hndlr.TypeKeys(p.getAttrs(i))
	    del names[0]
		
names = getNames('OCs.csv')
worker('Book1 - Excel', names)
