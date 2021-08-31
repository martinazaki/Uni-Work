#!/bin/sh

m=`ls -a | egrep ".snapshot\.[0-9]*" | wc -l`
echo "Creating snapshot $m"
mkdir ".snapshot.$m"
for file in *
do 
    if test "$file" != "snapshot-save.sh" -a "$file" != "snapshot-save.sh"
    then 
        cp "$file" "./.snapshot.$m/$file"
    fi 
done       