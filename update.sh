#!/bin/bash

#PRECONDITIONS: RUN AS ROOT SO SHUTDOWN WORKS

#if no updates are available, exit
#if no updates are available, that prints to stderr
if softwareupdate -l 2>&1 > /dev/null | grep 'No new software available.'; then
	echo "No updates are available."
	exit 0
fi


#change 3 to however many times users should be able to put off updating
for i in {3..0}; do
	echo "Welcome $i"
	python reminder.py $i

	#however long in seconds the program should wait before prompting the user again
	sleep 10
done

