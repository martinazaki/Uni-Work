//Martina Zaki z5264835

#include <stdio.h>

int main(void) {
    int number;
    printf ("Enter number: ");
    scanf ("%d", &number);

    int counter = 1;
    while (counter < number) {
        
        if (counter % 3 == 0 || counter % 5 == 0) {
            printf("%d\n", counter);
            
        }
        counter = counter + 1;
    
    }

    return 0;
}
