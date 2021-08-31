#!/bin/sh
m=`ls -a | egrep ".$1.[0-9]+" | wc -l`

cp "$1" ".$1.$m"
echo "Backup of '$1' saved as '.$1.$m'"