//Martina Zaki z5264835

#include <stdio.h>

int main (void) {
    printf("Enter integer: ");
    int number1;   
    scanf("%d", &number1);
    
    printf("Enter integer: ");
    int number2;   
    scanf("%d", &number2);
 
    printf("Enter integer: ");
    int number3;   
    scanf("%d", &number3);

    printf("The integers in order are: ");
    if (number1 <= number2 && number1 <= number3) {
        printf ("%d ", number1);
      
    } else if (number2 <= number3 && number2 <= number1) {
        printf ("%d ", number2);
        
    } else {
        printf ("%d ", number3);
    }
     
    if ((number1 >= number2 && number1 <= number3) || (number1 >= number3 && number1 <= number2)) {
      printf("%d ", number1);
      
    } else if ((number2 >= number1 && number2 <= number3) || (number2 >= number3 && number2 <= number1)) {
        printf ("%d ", number2);
      
    } else {
        printf ("%d ", number3); 
        
    } 
    
    if (number1 >= number3 && number1 >= number2) {
        printf ("%d\n", number1);
      
    } else if (number2 >= number3 && number2 >= number1) {
        printf ("%d\n", number2);
      
    } else {
        printf ("%d\n", number3);
      
    }
    
    return 0;
}
