#!/usr/bin/perl

$first = $ARGV[0];
$second = $ARGV[1];
$file = $ARGV[2];

open FILE, '>', "$file";
foreach $x ($first .. $second){
    print FILE "$x\n";
    $first++;
}

close FILE;