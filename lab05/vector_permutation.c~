#include <stdio.h>
#include <math.h>

#define MAX_SIZE 1000

void read_vectors(int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                 int vecotr_size );
                 
void change_vector (int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                    int vector_size, int changed_vector[MAX_SIZE]);
                    
int permutation_check (int vector2[MAX_SIZE], int vector_size);

int main (void) {

    int vector_size;
    int vector1[MAX_SIZE];
    int vector2[MAX_SIZE];
    int changed_vector[MAX_SIZE];
    
    printf("Enter vector length: ");
    scanf("%d",&vector_size);
    read_vectors(vector1, vector2, vector_size);
    int vadility = permutation_check (vector2, vector_size);
    if (vadility == 1) {
        printf("Invalid permutation\n");
        return 0;
    }
    
    change_vector(vector1, vector2, vector_size, changed_vector);
    
    printf("\n");
    
    return 0;
}


void read_vectors(int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                  int vector_size ) {
    int i = 0;
    printf("Enter vector: ");
    while(i < vector_size) {
        scanf("%d", &vector1[i]);
        i++;
    }
    i = 0; 
    printf("Enter permutation: ");
    while(i < vector_size) {
        scanf("%d", &vector2[i]);
        i++;
    }
    
    return; 
}

void change_vector (int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                    int vector_size, int changed_vector[MAX_SIZE]) {
                    
    
    int i = 0;
    while (i < vector_size) {
        changed_vector[i] = vector1[vector2[i]];
        
        i++;
    }
    
    i = 0;
    while (i < vector_size) {
        printf("%d ",changed_vector[i] );
        i++;
    }

    return;
}

int permutation_check (int vector2[MAX_SIZE], int vector_size) {
//check if permutation vector input was valid
    int i = 0;
    while (i < vector_size){
        if (vector2[i] < 0 || vector2[i] >= vector_size){
            return 1; 
        }
        i++;
    }

    return 0;
}
