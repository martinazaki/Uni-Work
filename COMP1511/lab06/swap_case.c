#include <stdio.h>

int main(void) {
    int upper(int character);
    int lower(int character);
    int character = getchar();
    while (character != EOF) {
        if (character >= 'a' && character <= 'z') {
            int first_character = upper(character);
            putchar(first_character);
       
        } else if (character >= 'A' && character <= 'Z') {
            int second_character = lower(character);
            putchar(second_character);
      
        } else {
            putchar(character);
        }
        
        character = getchar();
    }
    return 0;
}

int upper(int character) {

        int alphabetPosition = character - 'a';
        return 'A' + alphabetPosition;

}

int lower(int character) {

        int alphabetPosition = character - 'A';
        return 'a' + alphabetPosition;
    
}
