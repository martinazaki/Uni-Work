//Martina Zaki (z5264835)

#include <stdio.h>

#define MAX_LENGTH  100

int main (void) {
    int numbers[MAX_LENGTH] = {0};
    
    printf("Enter numbers forwards: \n");
    
    int i = 0;
    int valid_input = 1;
    while (valid_input == 1) {
        valid_input = scanf ("%d", &numbers[i]);
        i++;
    }
    
    printf("Reversed: \n");
    i = i - 2;
    while (i >= 0) {
        printf("%d\n", numbers[i]);
        i--;
    }
    
    return 0;
}
