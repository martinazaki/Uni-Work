#include <stdio.h>

int main(void) {  
    int lower;
    int upper;
    
    printf("Enter lower: ");
    scanf("%d", &lower);   
    printf("Enter upper: ");
    scanf("%d", &upper);
    
    int i = lower;
    while (i < upper - 1) {
      i = i+1;
      printf("%d\n", i);           
      
    }

   return 0;
}
