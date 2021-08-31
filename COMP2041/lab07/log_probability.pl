#!/usr/bin/perl

sub count_words {
	my ($find, $file) = @_;
	$counter = 0;	
	open F, $file or die;
        while ($line = <F>) {
                chomp $line;
		$line = lc $line;
                @words = grep(/./, split(/[^a-zA-Z]/, $line));
        	foreach $i (@words) {
                	if ($i =~ /^$find$/i) {
                        	$counter++;
                	}
        	}
        }
	return $counter;
}

sub total_words {
	my ($file) = @_;
	open F, $file or die;
	$counter = 0;
	while ($line = <F>) {
		chomp $line;
		@words = grep(/./, split(/[^a-zA-Z]/, $line));
		$counter += 0+@words;
	}
	return $counter;
}

foreach $file (glob "lyrics/*.txt") {	
	$cw = count_words(@ARGV[0], $file);
	$ncw = $cw + 1;
	$tw = total_words($file);
	$fq = log($ncw/$tw);
	@fn = split("/", $file);
	@ufn = split(".txt", @fn[1]);
	$artist = @ufn[0];
	$artist =~ s/_/ /g;
	
	printf("log((%d+1)/%6d) = %8.4f %s\n", $cw, $tw, $fq, $artist);
	
}