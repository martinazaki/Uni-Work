#include <stdio.h>

#include "get_string.h"

// print a line from stream using fgetc (only)
// reads  in at  most one less than size characters from stream and stores them into the
// buffer pointed to by s.  Reading stops after an EOF or a newline.  If a newline is read, it  is
// stored  into  the buffer.  A terminating null byte ('\0') is stored after the last character in the buffer.
void get_string(char *s, int size, FILE *stream) {

    int done = 0;
    int a;

    while (done < size - 1 && (a = fgetc(stream)) != EOF) {
        s[done] = a;
        done++;

        if (a == '\n') {
            break;
        }
    }
    s[done] = '\0';

}