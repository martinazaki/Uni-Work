//Martina Zaki (z5264835)

#include <stdio.h>
#define MAX_NUMBERS 1001
void print_divisble(int array_length, int array[]);
    int main(void) {
    int numbers[MAX_NUMBERS];
    int n;
    
    n = 0;
    while (n < MAX_NUMBERS && scanf("%d", &numbers[n]) == 1) {
        n = n + 1;
    }

    printf("Indivisible numbers:");
    print_divisble(n, numbers);
    
    return 0;
    }

// print integers in array which are not exactly divisible by any other integers in array

void print_divisble(int array_length, int array[]) {
    for (int i = 0; i < array_length; i++) {
        int factors = 0;
        for (int j = 0; j < array_length; j++) {
            if (array[i] % array[j] == 0) {
            factors++;
            }
            
        }
        
        if (factors == 1) {
            printf(" %d", array[i]);
        }
        
    }
    
    printf("\n");
}
