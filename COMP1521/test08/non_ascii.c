#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process(char *fname);

int main(int argc, char *argv[]) {
    for (int i = 1; i < argc; i++) {
        process(argv[i]);
    }
    return 0;
}    

void process(char *fname) {
    FILE *file = fopen(fname, "r");
    if (file == NULL) {
        perror(fname);
        exit(1);
    }

    ssize_t position = 0;
    int byte;

    while ((byte = fgetc(file)) != EOF) {
        if (byte > 127) {
            printf ("%s: byte %zd is non-ASCII\n", fname, position);
            return;
        }
        position++;
    }
    fclose(file);
    printf("%s is all ASCII\n", fname);
}