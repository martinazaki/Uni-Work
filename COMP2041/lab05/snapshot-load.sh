#!/bin/sh

m = `ls -a | egrep ".snapshot(\.[0-9])+" | wc -l`
echo "Creating snapshot $m"
mkdir ".snapshot.$m"
for file in *
do  
    if test "$file" != "snapshot-save.sh" -a "$file" != "snapshot-save.sh"
    then
        cp "$file" "./.snapshot.$m/$file"
    fi
done
echo "Restoring snapshot $1"
for file in "./.snapshot."$1"/"*
do
    name=`echo $file | cut -d '/' -f3`
    cp "$file" "$name"

done
