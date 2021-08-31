#!/usr/bin/perl

my @sortfile;
while ( ($line = <STDIN>) =~ /\S/ ) {
	chomp $line;
	@word = split /\s+/, $line;
	@word = sort @word;
	foreach my $w (@word) {
		print $w, " ";
	}
	print "\n";
}