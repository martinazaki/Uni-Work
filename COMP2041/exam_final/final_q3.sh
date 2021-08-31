#!/bin/dash

if [ -c == 2 ]
then
    cut -d '|' -f2 | uniq -i | cut -d "," -f1 | sort
fi