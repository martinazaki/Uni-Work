#!/usr/bin/perl

$found = lc @ARGV[0];
$counter = 0;

while ($line = <STDIN>) {
	chomp $line;
	$line = lc $line;
	@word = grep(/./, split(/[^a-zA-Z]/, $line));
	
	foreach $i (@word) {
		if ($i =~ /^$found$/i) {
			$counter++
		}
	}
}

print @ARGV[0], " occurred " , $counter, " times\n";