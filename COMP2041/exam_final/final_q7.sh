#!/bin/dash

awk '{for(i=p+1; i<$1;i++) print i} {p=$1}' $1