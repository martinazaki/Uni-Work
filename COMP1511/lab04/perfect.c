#include <stdio.h>

int main(void) {
    int x;
    printf("Enter number: ");
    scanf("%d", &x);
    printf("The factors of %d are: \n", x);
    
    int count = 1;
    int sum = 0;    
    
    
    while(count <= x) {
   
        if(x % count == 0) {
            printf("%d\n", count);
            sum = sum + count;
        }
        
       count = count + 1;
    }
    
    printf("Sum of factors = %d\n", sum);
    
    if(sum / x == 2) {
      printf("%d is a perfect number\n", x);
    } else {
      printf("%d is not a perfect number\n",x);
    }
    
    return 0;
}
