//Written by z5264835 (Martina Zaki)

#include <stdio.h>

int main (void) {
    printf ("How many scoops? ");
    
    int scoops;
    scanf ("%d", &scoops);
    printf ("How many dollars does each scoop cost? ");
    
    int dollars;
    scanf ("%d", &dollars);
    
    int totalmoney = scoops * dollars;
    if (10 >= totalmoney) {
        printf ("You have enough money!\n");
    } else {
        printf ("Oh no, you don't have enough money :(\n");
    }

    return 0;
}
