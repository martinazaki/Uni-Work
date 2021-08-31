#!/bin/dash
name=$1;
curl --location --silent http://www.timetable.unsw.edu.au/current/$1KENS.html | egrep "<a href=\"$1[0-9]*\.html\">[^<]*<" | sed 's/^ *//g' | sed 's/\.html//g' | sed 's/<//g' | sed 's/a href//g' | sed 's/td class="data">="//g' | sed 's/\/a>\/td>//g' | sed 's/>//g' | sed 's/"/ /g' | egrep -v "$name[0-9]{4} $name[0-9]{4}" | sort | uniq | sort