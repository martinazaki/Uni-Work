#include <stdio.h>

int main(void) {
   int number;
   printf("Enter year: ");
   scanf("%d", &number);
   
   if (number %  4 != 0) {
        printf ("%d is not a leap year.\n", number);
     
    } else if (number % 100 != 0) {
        printf ("%d is a leap year.\n", number);
     
    } else if (number % 400 != 0) {
        printf ("%d is not a leap year.\n", number);
     
    } else {
        printf ("%d is a leap year.\n", number);
     
    }
   
    return 0;
}
