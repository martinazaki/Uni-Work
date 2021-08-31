#!/usr/bin/perl

$i=0;
while (($s = <>) =~ /\S/ ) {
        push @lines, $s;
	$i+=1;
}

@printed = ();

while (@printed < $i) {
	$rn = int(rand($i));
	if($lines[$rn] ~~ @printed) {
        
	} else {
		print $lines[$rn];
                push @printed, $lines[$rn];
	}
}