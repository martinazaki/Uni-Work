// Calculates the straight-line distance between 2 points in Euclidean space

// Written by Martina 
// 19/03/2019

#include <stdio.h>
#include <math.h>

#define MAX_SIZE 1000

void read_vectors(int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                 int vecotr_size );

double calculate_distance (int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                           int vector_size);


int main (void) {

    int vector_size;
    int vector1[MAX_SIZE];
    int vector2[MAX_SIZE];
    
    printf("Enter vector length: ");
    scanf("%d",&vector_size);
    read_vectors(vector1, vector2, vector_size);
    double distance = calculate_distance (vector1, vector2, vector_size);
    printf("Euclidean distance = %lf\n",distance);

    
    return 0;
}

void read_vectors(int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                  int vector_size ) {
    int i = 0;
    printf("Enter vector 1: ");
    while(i < vector_size) {
        scanf("%d", &vector1[i]);
        i++;
    }
    i = 0; 
    printf("Enter vector 2: ");
    while(i < vector_size) {
        scanf("%d", &vector2[i]);
        i++;
    }
    return; 
}

double calculate_distance (int vector1[MAX_SIZE], int vector2[MAX_SIZE],
                           int vector_size) {
    double distance = 0;
    int counter = 0;
    while (counter < vector_size) {
        distance = distance + (vector1[counter] - vector2[counter])*
                   (vector1[counter] - vector2[counter]);
        counter++;
    }
    distance =  sqrt(distance);
    return distance;
}
