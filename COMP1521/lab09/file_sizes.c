#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

off_t calc(char *fname);

int main(int argc, char *argv[]) {
    off_t total = 0;    
    for (int i = 1; i < argc; i++) {
        total += calc(argv[i]);
    }
    
    printf("Total: %ld bytes\n", total);
    return 0;
}

off_t calc(char *fname) {
    struct stat m; 
    if (stat(fname, &m) != 0) {
        perror(fname);
        exit(1);
    }
    
    printf("%s: %ld bytes\n", fname, (long)m.st_size);
    return m.st_size; 
}