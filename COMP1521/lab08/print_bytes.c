#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

int main (int argc, char *argv[]) {

    char *name = argv[1];
    FILE *file = fopen(name, "r");

    if (file == NULL) {
        perror("Unable to open file");
        return 1;
    }
    
    int m = fgetc(file);
    int i = 0;
    while (m != EOF) {
        printf("byte %4d: %3d 0x%02x", i, m, m);
        if (isprint(m) != 0) {
            printf(" '%c'", m);

        }
        printf("\n");
        m = fgetc(file);
        i++;
    }

    fclose(file);
    
}