#!/bin/bash

#PRECONDITIONS: RUN AS ROOT SO SHUTDOWN WORKS

#check for connection errors
if softwareupdate -l 2>&1 > /dev/null | grep 'Can’t connect to the Apple Software Update server'; then
	echo "No internet connection."
	exit 0
fi


#if no updates are available, exit
#if no updates are available, that prints to stderr
if softwareupdate -l 2>&1 > /dev/null | grep 'No new software available.'; then
	echo "No updates are available."
	exit 0
fi



#install all updates but will not restart, store output
softwareupdate -i -a > log.txt

#see if the restart is needed
if grep -Fxq "You have installed one or more updates that requires that you restart your computer" log.txt
	then
		#change 3 to however many times users should be able to put off updating
		for i in {3..0}; do
			#echo "Welcome $i"
			python reminder.py $i

			#however long in seconds the program should wait before prompting the user again
			sleep 10
		done
	else
		echo "no restart needed"
		exit 0
fi
