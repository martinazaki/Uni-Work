#!/bin/sh

# Demo01.sh from part of jpg2png.sh Lab03 COMP2041 20T2
# Martina Zaki, z5264835

for file in *
do
	ext=`echo $file | cut -d'.' -f2`
	fn=`echo $file | cut -d'.' -f1`
done