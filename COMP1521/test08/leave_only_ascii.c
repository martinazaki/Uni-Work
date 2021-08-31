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

    char *suffix = ".tmp.leave_only_ascii";
    char temp[strlen(fname) + strlen(suffix) + 1];
    strcpy(temp, fname);
    strcpy(temp, suffix);

    FILE *name = fopen(temp, "w");
    if (name == NULL) {
        perror(fname);
        exit(1);
    }

    int byte;
    while ((byte = fgetc(file)) != EOF) {
        if (byte <= 127) {
            fputc(byte, name);
        }
    }
    fclose(file);
    fclose(name);

    if (rename(temp, fname) != 0) {
        perror("rename");
        exit(1);
    }
}    