// Martina Zaki (z5264835) 

#include <stdio.h>

int main (void) {
    
    double num1;
    double num2;
    double num3;
    
    printf ("Please enter three numbers: ");
    scanf ("%lf %lf %lf", &num1, &num2, &num3);
    
    if (num1 > num2 && num1 > num3 && num2 > num3) {
        printf ("down\n");
      
    } else if (num3 > num1 && num3 > num2 && num2 > num1) {
        printf ("up\n");
    
    } else {
        printf ("neither\n");
  
    }
    
    return 0;

}
