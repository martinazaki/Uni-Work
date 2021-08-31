#include <stdio.h>

int main(void) {
    int size;
    int x = 1;
    int y = 1;
    
    printf("Enter size: ");
    scanf("%d", &size);
    
    while(y <= size) {
    x = 1;
      while(x <= y) {
        if(x == 1 || x == y || y == size) {
          printf("*");
        
        } else {
          printf(" ");
        
        }
        
        x++;
        
      }
      
      y++;
      printf("\n");
    
    }

    return 0;
}
