#!/usr/bin/python

import os
os.putenv("DISPLAY",":0.0")

from BeautifulSoup import BeautifulSoup
import re
from urllib2 import urlopen
from urllib import urlretrieve
import string
import sys
import pygtk
import pynotify

url = "http://spin.ecn.purdue.edu/ece302/"
base = "/home/kuroshi/Documents/School/ECE 302/"
homework = "homework"
solutions = "homework/solutions"
lectures = "lectures"
project = "proj"
exam = "Exam "
documents = "documents"


def main(url, base):
	#Sets up libnotify
	pynotify.init("Basics")

	#Sets up the site....
	exists = 0

	page = urlopen(url)
	soup = BeautifulSoup(page)
	items = soup.findAll(id='notes')

	#Downloads exam information...
	ecount = 0
	rows = items[0].findAll('tr')
	rows.pop(0)
	for eNum,row in enumerate(rows, start=1):
		links = row.findAll('a')
		for link in links:
			exa = str(link).encode('ascii', 'ignore').split("\"")[1]
			filename = exa.split("Exams/exam" + str(eNum) + "/")[1]
			if not os.path.exists(base + exam + str(eNum)):
				os.makedirs(base + exam + str(eNum))
			for curExam in os.listdir(base + exam + str(eNum)):
				if curExam == filename:
					exists = 1
			if exists == 0:
				urlretrieve(url + exa, base + exam + str(eNum) + "/" + filename)
				ecount = ecount + 1
				if ecount == 1:
					ex = filename
			exists = 0


	#Downloads projects...
	pcount = 0
	rows = items[1].findAll('tr')
	rows.pop(0)
	for pNum,row in enumerate(rows, start=1):
		links = row.findAll('a')
		for link in links:
			pro = str(link).encode('ascii', 'ignore').split("\"")[1]
			filename = pro.split("Projects/project" + str(pNum) + "/")[1]
			if not os.path.exists(base + project + str(pNum)):
				os.makedirs(base + project + str(pNum))
			for curPro in os.listdir(base + project + str(pNum)):
				if curPro == filename:
					exists = 1
			if exists == 0:
				urlretrieve(url + pro, base + project + str(pNum) + "/" + filename)
				pcount = pcount + 1
				if pcount == 1:
					proj = filename
			exists = 0

	#Downloads homework and solutions...
	hcount = 0
	scount = 0
	modcount=0
	links = items[2].findAll('a')
	for link in links:
		hw = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = hw.split("HW/")[1]
		if (modcount % 2 == 0):
			for curHw in os.listdir(base + homework):
				if curHw == filename:
					exists = 1
			if exists == 0:
				urlretrieve(url + hw, base + homework + "/" + filename)
				hcount = hcount+1
				if hcount == 1:
					hwl = filename
			exists = 0
			modcount = modcount + 1
		else:
			for curSol in os.listdir(base + solutions):
				if curSol == filename:
					exists = 1
			if exists == 0:
				urlretrieve(url + hw, base + solutions + "/" + filename)
				scount = scount+1
				if scount == 1:
					soln = filename
			exists = 0
			modcount = modcount + 1

	#Downloads lecture notes...
	links = items[3].findAll('a')
	lcount = 0
	for link in links:
			note = str(link).encode('ascii', 'ignore').split("\"")[1]
			filename = note.split("Notes/")[1]
			for curNote in os.listdir(base + lectures):
				if curNote == filename:
					exists = 1
			if exists == 0:
				urlretrieve(url + note, base + lectures + "/" + filename)
				lcount = lcount+1
				if lcount == 1:
					lec = filename
			exists = 0

	#Sends our notifications...
	notifyString = ""
	if lcount == 1:
		notifyString = notifyString + "\nLecture note document " + lec + "."
	elif lcount > 1:
		notifyString = notifyString + "\n" + str(lcount) + " lecture note documents."
	if hcount == 1:
		notifyString = notifyString + "\nHomework " + hwl + "."
	elif hcount > 1:
		notifyString = notifyString + "\n" + str(hcount) + " homework documents."
	if scount == 1:
		notifyString = notifyString + "\nSolution " + soln + "."
	elif scount > 1:
		notifyString = notifyString + "\n" + str(scount) + " homework solution documents."
	if pcount == 1:
		notifyString = notifyString + "\nProject file " + proj + "."
	elif pcount > 1:
		notifyString = notifyString + "\n" + str(pcount) + " project files."
	if ecount == 1:
		notifyString = notifyString + "\nExam file " + ex + "."
	elif ecount > 1:
		notifyString = notifyString + "\n" + str(ecount) + " exam files."

	if lcount > 0 or hcount > 0 or scount > 0 or pcount > 0 or ecount > 0:
		n = pynotify.Notification("Downloaded ECE 302 Documents", notifyString)
		n.show()

if __name__ == "__main__":
	main(url, base)
