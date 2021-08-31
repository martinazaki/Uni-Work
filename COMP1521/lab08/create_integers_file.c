#include <stdio.h>
#include <stdlib.h>

int main (int argc, char *argv[]) {

    char *name = argv[1];
    FILE *file = fopen(name, "w");

    if (file == NULL) {
        perror("Unable to open file");
        return 1;
    }

    int i = atoi(argv[2]);
    while (i <= atoi(argv[3])) {
        fprintf(file, "%d\n", i);
        i++;
    }

    fclose(file);
    
}