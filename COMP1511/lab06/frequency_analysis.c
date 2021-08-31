#include <stdio.h>
#define ASCII   127

int main (void) {
    double letters[ASCII] = {0};
    double freq = 0;
    int c = getchar();
    double total = 0;
    while(c != EOF){
        if(c >= 'A' && c <= 'Z'){
            c = c - ('A'- 'a');
            total++;
            letters[c]++;
        } else if(c >= 'a' && c <= 'z') {
            total++;
            letters[c]++;
        }
        c = getchar();
        
    }
    c = 'a';
    while (c <= 'z') {
    
        if(c >= 'a' && c <= 'z') {
            freq = letters[c] / total;
        
        }
        printf("'%c' %lf %.0lf \n", c, freq, letters[c]);
        c++;
    }
    
    return 0;
}
