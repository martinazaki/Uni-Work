//Martina Zaki (z5264835)

#include <stdio.h>
#include <assert.h>

#define MAX_LINE_CHARS 256
int main(void) {
    char line[MAX_LINE_CHARS] = {0};
    
    fgets(line, MAX_LINE_CHARS, stdin);
    
    int i = 0;
    scanf("%d", &i);
    assert(i >= 0 && i < MAX_LINE_CHARS);
    printf("The character in position %d is '%c'\n", i, line[i]);
    
    return 0;
}
