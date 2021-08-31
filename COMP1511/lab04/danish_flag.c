#include <stdio.h>

int main(void) {
    int size;   
    printf("Enter the flag size: ");
    scanf("%d", &size);

    int x = 1;
    while(x <= size * 4) {
        int y = 1;
        while(y <= size*9) {
            if (y == size*3 || y == size*3+1 || x == (size*2)+1 || x == size*2) {
                printf(" ");
            
            } else {
                printf("#");
       
            }
             y = y + 1;
        }
        
    x = x + 1;
    printf("\n");
    }  

    return 0;
}


