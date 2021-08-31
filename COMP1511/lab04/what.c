//Martina Zaki (z5264835)

#include <stdio.h>

#define MAX_LENGTH  100

int main (void) {
    int numbers[MAX_LENGTH];
    
    printf("Enter numbers forward:\n");
    
    int i = 0;
    int valid_input = 1;
    while (valid_input == 1) {
        valid_input = scanf ("%d", &numbers[i]);
        i++;
    }
    
    
    return 0;
}
