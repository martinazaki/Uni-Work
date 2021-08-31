//Martina Zaki z5264835

#include <stdio.h>

int main(void) {
    int total;
    int marks;
    
    printf ("Enter the total number of marks in the exam: "); 
    scanf ("%d", &total);
    
    printf ("Enter the number of marks the student was awarded: ");
    scanf ("%d", &marks);
    
    double percent =  (marks * 100.0 / total);
    
    printf ("The student scored %.lf%% in this exam.\n", percent);
    
    return 0;
}
