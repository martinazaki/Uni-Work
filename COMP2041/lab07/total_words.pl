#!/usr/bin/perl

$total = 0;
while ( ($line = <STDIN>) ) {
      	chomp $line;
	@words = grep(/./, split(/[^a-zA-Z]/, $line));
	$total += 0+@words;
}

print $total, " words\n";