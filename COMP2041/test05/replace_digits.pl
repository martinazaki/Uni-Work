#!/usr/bin/perl -w

foreach $file (@ARGV) {
    open my $fi, '<', $file or die "Can not open $file: $!";
    @lines = <$fi>;
    close $fi;

    foreach $line (@lines) {
        $line =~ s/\d/#/g;
    }

    open my $m, '>', $file or die "Can not open $file: $!";
    print $m @lines;
    close $m;
}