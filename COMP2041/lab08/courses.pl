#!/usr/bin/perl -w 
my %hasharray;
$code = shift @ARGV;
$codey = $code.'KENS';
use LWP::Simple;
$url = "http://www.timetable.unsw.edu.au/current/$codey.html";
$web_page = get($url) or die "Unable to get $url";
@arrays = $web_page =~ /<a href="$code[0-9]{4}\.html">[^<]*</g;
foreach $str (@arrays) {
    $str =~ s/\.html">/ /g;
    $str =~ s/<//g;
    $str =~ s/a href="//g;
    if ($str !~ /$code[0-9]{4} $code[0-9]{4}/){ push(@array,$str) };
}
@array = sort @array;
foreach $int (@array) { 
    $hasharray{$int}++;
}
foreach (sort keys %hasharray) {
    print "$_\n";
}