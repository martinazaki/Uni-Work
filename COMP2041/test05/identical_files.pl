#!/usr/bin/perl -w

if (($#ARGV + 1) < 2) {
    print "Usage: $0 <files>\n";
} else {
    $first = "$ARGV[0]";
    open FILE, "<", $first or die;
    @orig = <FILE>;
    close FILE;
    
    @argv = @ARGV;
    splice @argv, 0, 1;
    
    foreach $file (@argv) {
        open FILE, "<", $file or die;
        
        @compare = <FILE>;
        if ($#orig != $#compare) {
            print "$file is not identical\n";
            exit 1;
        } else {
            $count = 0;
            while ($count < $#orig + 1) {
                $original_line = $orig[$count];
                $compare_line = $compare[$count];
                
                if ($original_line ne $compare_line) {
                    print "$file is not identical\n";
                    exit 1;
                }
                
                $count++;
            }
        }
        close FILE;
    }
}

print "All files are identical\n";