#!/usr/bin/perl -w

foreach $file (@ARGV) {
    open my $f, '<', $file or die "Error cannot open $file";
    @line = <$f>;
    close $f;

    foreach $line (@line) {
        $line =~ s/(\S+) (\S+)/$2 $1/;
    }
    open my $m, '>', $file or die "Error cannot open $file";
    print $m @line;
    close $m
}
