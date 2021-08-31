#include <stdio.h>

int is_vowel(char c);

int main(void) {
    char c = getchar();
    while(c != EOF) {
        int vowel = is_vowel(c);
        if(vowel != 1) {
            putchar(c);
            
        }
        c = getchar();
    }
    
    return 0;
}

int is_vowel(char c) {
    if(c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
        return 1;
        
    }
    
    return 0;
}
