#!/bin/sh

file="$1"

info=`cat $file`

echo "$info" | egrep "\"price\": " | cut -d',' -f'1' | sed "s/^ *{\"name\": \"//" | sed "s/\" *$//" | sort | uniq | sort