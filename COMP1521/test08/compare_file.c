#include <stdio.h>
#include <stdlib.h>

int comp(char *fname1, char *fname2);

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <file1> <file2>\n", argv[0]);
        return 1;
    }
    return comp(argv[1], argv[2]);
}

int comp(char *fname1, char *fname2) {
    FILE *file = fopen(fname1, "r");
    if (file == NULL) {
        perror(fname1);
        return 1;
    }

    FILE *files = fopen(fname2, "r");
    if (files == NULL) {
        perror(fname2);
        return 1;
    }

    ssize_t position = 0;
    int byte1;
    int byte2;

    while (1) {
        byte1 = fgetc(file);
        byte2 = fgetc(files);
        if (byte1 != byte2 || byte1 == EOF) {
            break;
        }
        position++;
    }

    if (byte1 == byte2) {
        printf ("Files are identical\n");

    } else if (byte1 == EOF) {
        printf ("EOF on %s\n", fname1);

    } else if (byte2 == EOF) {
        printf ("EOF on %s\n", fname2);

    } else {
        printf ("Files differ at byte %zd\n", position);

    }

    fclose(file);
    fclose(files);
    return 0;
}