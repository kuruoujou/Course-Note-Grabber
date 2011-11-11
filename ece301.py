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

home = "https://engineering.purdue.edu/~chihw/11ECE301F/11ECE301F.html"
docs = "https://engineering.purdue.edu/~chihw/11ECE301F/co_desc.html"
notes = "https://engineering.purdue.edu/~chihw/11ECE301F/co_lec.html"
homework = "https://engineering.purdue.edu/~chihw/11ECE301F/co_hw.html"
exams = "https://engineering.purdue.edu/~chihw/11ECE301F/com/sample_exams.html"
formulas = "https://engineering.purdue.edu/~chihw/11ECE301F/com/formula_tables.html"
base = "/home/kuroshi/Documents/School/ECE 301/"
examFile = "Exams"
docsFile = "Documents"
lecFile = "Lecture Notes"
hwFile = "Homework"
fmFile = "Forumula tables"
seFile = "Sample Exams"

def main(base):
	#Sets up libnotify
	pynotify.init("Basics")
	exists = 0

	#Downloads past and upcoming exam info...
	page = urlopen(home)
	soup = BeautifulSoup(page)
	links = soup.findAll(href=re.compile('.*?\.pdf'))
	eicount = 0
	for link in links:
		ei = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = ei.split("/")[-1]
		for curEi in os.listdir(base + examFile):
			if curEi == filename:
				exists = 1
		if exists == 0:
			urlretrieve(home + ei, base + examFile + "/" + filename)
			eicount = eicount+1
			if eicount == 1:
				eil = filename
		exists = 0

	#Downloads Course Docs
	page = urlopen(docs)
	soup = BeautifulSoup(page)
	links = soup.findAll(href=re.compile('.*?\.pdf|.*?\.html?'))
	dcount = 0
	for link in links:
		doc = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = doc.split("/")[-1]
		for curDoc in os.listdir(base + docsFile):
			if curDoc == filename:
				exists = 1
		if exists == 0:
			urlretrieve(docs + doc, base + docsFile + "/" + filename)
			dcount = dcount+1
			if dcount == 1:
				docl = filename
		exists = 0

	#Downloads Lecture Notes
	page = urlopen(notes)
	soup = BeautifulSoup(page)
	links = soup.findAll(href=re.compile('.*?\.pdf|.*?\.html?'))
	ncount = 0
	for link in links:
		note = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = note.split("/")[-1]
		for curNote in os.listdir(base + lecFile):
			if curNote == filename:
				exists = 1
		if exists == 0:
			urlretrieve(notes + note, base + lecFile + "/" + filename)
			ncount = ncount+1
			if ncount == 1:
				notel = filename
		exists = 0

	#Downloads Homeworks, Projects, and Solutions
	page = urlopen(homework)
	soup = BeautifulSoup(page)
	links = soup.findAll(href=re.compile('.*?\.pdf|.*?\.html?'))
	hcount = 0
	for link in links:
		hw = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = hw.split("/")[-1]
		for curHw in os.listdir(base + hwFile):
			if curHw == filename:
				exists = 1
		if exists == 0:
			urlretrieve(homework + hw, base + hwFile + "/" + filename)
			hcount = hcount+1
			if hcount == 1:
				hwl = filename
		exists = 0

	#Downloads Sample Exams
	page = urlopen(exams)
	soup = BeautifulSoup(page)
	links = soup.findAll(href=re.compile('.*?\.pdf|.*?\.html?'))
	secount = 0
	for link in links:
		sexam = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = sexam.split("/")[-1]
		for curSexam in os.listdir(base + seFile):
			if curSexam == filename:
				exists = 1
		if exists == 0:
			urlretrieve(exams + sexam, base + seFile + "/" + filename)
			secount = secount+1
			if secount == 1:
				sel = filename
		exists = 0

	#Downloads Formula Tables
	page = urlopen(formulas)
	soup = BeautifulSoup(page)
	links = soup.findAll(href=re.compile('.*?\.pdf|.*?\.html?'))
	fcount = 0
	for link in links:
		fm = str(link).encode('ascii', 'ignore').split("\"")[1]
		filename = fm.split("/")[-1]
		for curFm in os.listdir(base + fmFile):
			if curFm == filename:
				exists = 1
		if exists == 0:
			urlretrieve(formulas + fm, base + fmFile + "/" + filename)
			fcount = fcount+1
			if fcount == 1:
				forml = filename
		exists = 0

	#Sends our notifications...
	notifyString = ""
	if eicount == 1:
		notifyString = notifyString + "\nExam information document " + eil + "."
	elif eicount > 1:
		notifyString = notifyString + "\n" + str(eicount) + " exam information documents."
	if dcount == 1:
		notifyString = notifyString + "\nCourse document " + docl + "."
	elif dcount > 1:
		notifyString = notifyString + "\n" + str(dcount) + " course documents."
	if ncount == 1:
		notifyString = notifyString + "\nLecture note document " + notel + "."
	elif ncount > 1:
		notifyString = notifyString + "\n" + str(ncount) + " lecture note documents."
	if hcount == 1:
		notifyString = notifyString + "\nHomework document " + hwl + "."
	elif hcount > 1:
		notifyString = notifyString + "\n" + str(hcount) + " homework documents."
	if secount == 1:
		notifyString = notifyString + "\nSample exam file " + sel + "."
	elif secount > 1:
		notifyString = notifyString + "\n" + str(secount) + " sample exam files."
	if fcount == 1:
		notifyString = notifyString + "\nFormula file " + forml + "."
	elif fcount > 1:
		notifyString = notifyString + "\n" + str(fcount) + " formula files."

	if eicount > 0 or dcount > 0 or ncount > 0 or hcount > 0 or secount > 0 or fcount > 0:
		n = pynotify.Notification("Downloaded ECE 301 Documents", notifyString)
		n.show()

if __name__ == "__main__":
	main(base)
