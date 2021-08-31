//Written by z5264835 (Martina Zaki)

#include <stdio.h>

int main() {
    printf ("Please enter two integers:");
    
    int num1, num2;
    scanf ("%d %d", &num1, &num2);
    
    int sum;
    sum = num1 + num2;
    
    printf("%d + %d = %d\n", num1, num2, sum);

    return 0;
}
