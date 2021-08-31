#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[]) {

    char *name = argv[1];
    FILE *file = fopen(name, "w");

    if (file == NULL) {
        perror("Unable to open file");
        return 1;
    }

    int i = 2;
    while (i < argc) {
        fputc(atoi(argv[i]), file);
        i++;
    }
    return 0;    
}