#include <stdio.h>
#include <stdlib.h>
#include <math.h>


int main(int argc, char *argv[]) { 
    char c = getchar();
    int shift = atoi(argv[1]);
    while(shift < 0 ) {
        shift = shift + 26;
    }
    
    while (c != EOF) {
        if(c >= 'A' && c <= 'Z') {
            c = abs(c - 'A' + shift );
            c = c % 26;
            c = c + 'A';
            
        } else if (c >= 'a' && c <= 'z') {
            c = abs(c - 'a' + shift );
            c = c % 26;
            c = c + 'a';
        
        }
        putchar(c);
        c = getchar();
    
    }
    
    return 0;
}
