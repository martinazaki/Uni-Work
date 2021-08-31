//Martina Zaki (z5264835)

#include <stdio.h>

#define MAX_LINE_CHARS 4096

int main(void) {
    char line[MAX_LINE_CHARS];

    while (fgets(line, MAX_LINE_CHARS, stdin) != NULL) {

        int size = 0;
        while ((line[size] != '\n') && (line[size] != '\0')) {
            size = size + 1;
        }

        int j = size - 1;
        while (j >= 0) {
            printf("%c", line[j]);
            j = j - 1;
        }
        printf("\n");
    }

    return 0;
}
