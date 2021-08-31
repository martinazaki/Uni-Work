#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void filemode(char *fname);

int main(int argc, char *argv[]) {   
    for (int i = 1; i < argc; i++) {
        filemode(argv[i]);
    }
    return 0;
}

void filemode(char *fname) {
    struct stat m; 
    if (stat(fname, &m) != 0) {
        perror(fname);
        exit(1);
    }
    
    mode_t n = m.st_mode;

    char per[] = "?rwxrwxrwx";
    int n_per = strlen(per);

    if (S_ISREG(n)) {
        per[0] = '-';
    } else if (S_ISDIR(n)) {
        per[0] = 'd';
    }

    for (int j = 1; j < n_per; j++) {
        if (!(n & (1 << (j - 1)))) {
            per[n_per - j] = '-';
        }
    }
    printf("%s %s\n", per, fname);
}