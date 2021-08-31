#!/usr/bin/perl -w

# sheeple.pl by Martina Zaki, z5264835

while ($line = <>) {
    
    # SUBSET 0
    # Used Andrew's lecture
    $line =~ s?^#!.*?#!/usr/bin/perl -w?;
    $line =~ s?echo (.*)?print "$1\\n";?;
    $line =~ s?^ (.*)?system "$1\\n"?;
    $line =~ s?^ (.*)=(.*)?$/$1 = '$1\\n'?; 
    
    
    # SUBSET 1
    $line =~ s?cd (.*)?chdir '$1\\n';?;

    if ($line =~ / *for (.*) in (.*)/) {
        $var = $line;
        $var =~ s/ *for (.*) in (.*)/$1/;
    }

    print $line;
}