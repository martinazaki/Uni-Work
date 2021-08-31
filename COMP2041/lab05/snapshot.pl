#!/usr/bin/perl -w
use strict;
use Cwd;
use File::Basename;

my $action = $ARGV[0];
my $dirname = ".snapshot";
my $backup_no = 0;
my $flag = 0;
my $newdir;

sub load{
    my $n = $_[0];
    my $curr_dir = getcwd();
    foreach my $f (glob "$dirname.$n/*"){
        my $base_file = basename($f);
        open F_R, '<', "$f", or die "Cant open read file";
        open F_W, '>', "$curr_dir/$base_file" or die "Cant open write file";
        next if ($f eq "snapshots.pl");
         foreach my $line (<F_R>){
            print F_W $line;
        }
        close(F_R);
        close(F_W);
    }
    print "Restoring snapshot $n\n";

}

sub save{
    while( $flag == 0 ){ 
        $newdir = "$dirname.$backup_no";
        if ( -e $newdir and -d $newdir){
                $backup_no++;
                $newdir = "$dirname.$backup_no";
        }else{
               $flag = 1;
               mkdir $newdir;
               
               foreach my $read_file (glob "*"){
                   next if ($read_file eq "snapshots.pl");
                   open FILE_R, '<', "$read_file", or die "Cant open read file";
                   open FILE_W, '>', "$newdir/$read_file" or die "Can't open write file";
                    foreach my $line (<FILE_R>){
                        print FILE_W $line;
                    }
                    close(FILE_R);
                    close(FILE_W);
                    unlink $read_file;
                }
                print "Creating snapshot $backup_no\n";
        }    
    }   
}

if ($action eq "save"){ 
    save();
}
else{
    save();
    my $n = $ARGV[1];
    load($n);
}