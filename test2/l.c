#include <stdio.h>

int main(void) {
    int size;
    printf("Enter size: ");
    scanf("%d", &size);
    
    int i = 1;
    while(i <= size) {
      int j = 1;
      while(j <= size) {
        if(i == j) {
          printf("*");
          
        } else if(i == size) {
          printf("*");
        
        } else if(i == size && j == size - 1) {
          printf("*");
          
        }
        
        j++;
      
      }
      
      i++;
      printf("\n");
    
    }

    return 0;
}
