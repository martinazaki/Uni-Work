#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) {
    char *value = getenv("HOME");
    char buffer[50];
    snprintf(buffer, 50, "%s/.diary", value);
    FILE *diary = fopen(buffer, "a");
        if (diary == NULL) {
            perror("Unable to open file");
            return 1;
        }
        
        int i = 1;
        while(i < argc) {
            fprintf(diary, "%s ", argv[i]);
            i++;
        }

        fprintf(diary, "\n");

    return 0;
}