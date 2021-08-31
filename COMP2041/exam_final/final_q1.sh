#!/bin/dash

cut -d '|' -f3 | uniq | cut -d " " -f2 | sort