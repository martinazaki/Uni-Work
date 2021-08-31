#include <stdio.h>

    int main(){
    printf("Enter your age: ");
    int number;
    scanf("%d", &number);
    
    int lower = number/2 + 7;
    int upper = ((number - lower) *2) + number;
    
    int diff1 = number - lower;
    if(diff1<1){
        printf("You are too young to be dating.\n");
    }

    else{
        printf("Your dating range is %d to %d years old.\n", lower, upper);
    }
    return 0;
    } 
