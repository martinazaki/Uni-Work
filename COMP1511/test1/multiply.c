// Martina Zaki (z5264835)

#include <stdio.h>

int main (void) {
    
    int x;
    int y;
    
    scanf("%d %d", &x, &y);
    
    int multiply = x * y;
    
    if (multiply > 0) {
        printf ("%d\n",  multiply);
        
    } else if (multiply < 0) {
        printf("%d\n", -1*multiply);
    
    } else {
        printf("zero\n");
    
    }

    return 0;

}
