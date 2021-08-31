#!/usr/bin/perl -w
use strict;

my $file = $ARGV[0];
my $flag = 0;
my $backup_no = 0;
my $newfile = ".$file.$backup_no";

while ($flag == 0){

     if ( -e $newfile){
        $backup_no++;
        $newfile = ".$file.$backup_no";
     }else{
        $flag = 1;
        open FILE_R, '<', "$file" or die "Couldn't open file for reading";
        open FILE_W, '>', "$newfile" or die "Couldn't open file for reading";
        foreach my $line (<FILE_R>){
            print FILE_W $line;
        }
        close (FILE_R);
        close (FILE_W);
        print "Backup of '$file' saved as '$newfile'\n";
    }
}