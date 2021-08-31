#!/bin/dash

first=$1
second=$2

for arg in "$@"
do 
    # if first file is repeated then print
    if ($first = $second)
    then
        echo "ln -s $1 $2\n"
    else
        echo "No files can be replaced by symbolic links"
    fi

done