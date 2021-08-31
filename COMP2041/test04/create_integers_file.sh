#!/bin/bash

first=$1
second=$2
file=$3

while test $second -ge $first
do
    echo "$first">>"$file"
    first=`expr $first + 1`

done