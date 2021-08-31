#include <stdio.h>

int main(void) {
    int size;
    printf("Enter size: ");
    scanf("%d", &size);
    
    int i = 1;
    while(i <= size) {
        int j = 1;
        while(j <= size) {
            if(i == j || i+j == size+1) {
            printf("*");
            } else {
            printf("-");
            }
            j = j + 1;
        }
    
        i = i + 1;
        printf("\n");
    }

    return 0;
}
