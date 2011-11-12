#!/bin/bash

#Runs all python scripts in this directory.

#Change to your grabber directory. STAR IS IMPORTANT, DO NOT REMOVE.
for SCRIPT in /home/kuroshi/scripts/courseNoteGrabber/* ; do
	if [ "$SCRIPT" != "/home/kuroshi/scripts/courseNoteGrabber/runAll.sh" ]; then
		if [ -f $SCRIPT -a -x $SCRIPT ]; then
			$SCRIPT
		fi
	fi
done
