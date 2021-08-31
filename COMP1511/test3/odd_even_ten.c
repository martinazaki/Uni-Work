//Martina Zaki (z5264835)

#include <stdio.h>

int main (void) {

    int array[10];
    int i;
    int num = 10;

    for (i = 0; i < num; i++) {
        scanf("%d", &array[i]);

    }

    printf("Odd numbers were: ");

    for (i = 0; i < num; i++) {
        if (array[i] % 2 != 0) {
            printf("%d ", array[i]);

        }

    }
    
    printf("\nEven numbers were: ");
    
    for (i = 0; i < num; i++) {
        if (array[i] % 2 == 0) {
            printf("%d ", array[i]);

        }

    }
    
    printf("\n");
}
