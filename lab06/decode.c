#include <stdio.h>
#include <stdlib.h>

char cipher(char c, char subs[]);

int main(int argc, char *argv[]) { 
    
    
    char c = getchar();
    while (c != EOF) {
        if(c >= 'A' && c <= 'Z'){
            c = c - 'A' + 'a';
            c = cipher(c, argv[1]);
            c = c + 'A';
        }else if (c >= 'a' && c <= 'z') {
            c = cipher(c, argv[1]);
            c = c + 'a';
        }
        putchar(c);
        c = getchar();
    }
    
    return 0;
}

char cipher(char c, char subs[]){
    
    int i = 0;
    while (i < 26) {
        if(c == (subs[i])) {
            break;
        }
        
        i++;
    }
    
    if (i < 26){
        return i;
    } else { 
        return c;
    }
}
