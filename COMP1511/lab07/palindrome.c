#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define MAX_SIZE    4096

int main (void) {
    char c[MAX_SIZE];
    printf ("Enter a string: ");
    fgets (c, MAX_SIZE -1, stdin);
    int count = strlen(c) - 1;
    int end = count - 1;
    int middle = count/2;
    
    int begin = 0;
    for (begin = 0; begin < middle; begin++) {
        if (c[begin] != c[end]) {
            printf ("String is not a palindrome\n");
            break;
        
        }
        end--;
        
    }
    
    if (begin == middle) {
        printf ("String is a palindrome\n");
    
    }
   
    return 0;  
}   
