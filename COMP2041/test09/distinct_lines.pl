#!/usr/bin/perl

$p = $ARGV[0];
$done = 0;
$number = 0;

%read;
while ($line = <STDIN>) {
	# transform line
	$line =~ s/ //g;
	$line =~ tr/[A-Z]/[a-z]/;

	if (exists($read{$line})) {
		$read{$line}++;
	} else {
		$number++;
		$read{$line}++;
	}
	$done++;
	
	if ($number == $p) {
		print "$number distinct lines seen after $done lines read.\n";
		exit;
	}
}

print "End of input reached after $done lines read - $p different lines not seen.\n";