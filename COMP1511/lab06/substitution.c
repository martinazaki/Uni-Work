#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[]) { 
    
    
    char c = getchar();
    while (c != EOF) {
        if(c >= 'A' && c <= 'Z') {
            c = c - 'A';
            int x = c;
            c = argv[1][x];
            c = c - 'a' + 'A';
        } else if (c >= 'a' && c <= 'z') {
            c = c - 'a';
            int x = c;
            c = argv[1][x];
        }
        putchar(c);
        c = getchar();
    }
    
    return 0;
}
