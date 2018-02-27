#!/bin/bash

#check for updates
#if no updates are available, exit



#change 3 to however many times users should be able to put off updating
for i in {3..0}; do
	echo "Welcome $i"
	python reminder.py $i

	#however long in seconds the program should wait before prompting the user again
	sleep 10
done

