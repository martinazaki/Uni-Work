// Written by Martina Zaki, z5264835

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "lengthDefinitions.h"
#include "searchPagerank.h"

#define MAX_LINE_RESULT 30

int main(int argc, char* argv[]) {
  int number_of_urls = numberOfURLS();
  indexList* list = invertedIndexDetails(number_of_urls);
  if (argc > 1) {
    char string[MAX_LENGTH_LINE];
    FILE* filename = fopen("invertedIndex.txt", "r");
    int i;
    int j;
    char key[MAX_LENGTH_URL + 1];

    while (fgets(string, MAX_LENGTH_LINE, filename) != NULL) {
      for (i = 1; i < argc; i++) {
        strcpy(key, argv[i]);
        strcat(key, " ");
        if (strstr(string, key) == string) {
          for (j = 0; j < number_of_urls; j++) {
            if (strstr(string, list[j].URL) != NULL) {
              list[j].searchPR += 1;
            }
          }
        }
      }
    }
    fclose(filename);
  }
  list = invertedIndexSorted(list, number_of_urls);
  showInvertedIndex(list, number_of_urls);
  free(list);
  return EXIT_SUCCESS;
}

int numberOfURLS() {
  int number_of_urls = 0;
  char string[MAX_LENGTH_LINE];
  FILE* filename = fopen("pagerankList.txt", "r");
  while (fgets(string, MAX_LENGTH_LINE, filename) != NULL) {
    number_of_urls++;
  }
  fclose(filename);
  return number_of_urls;
}

indexList* invertedIndexDetails(int number_of_urls) {
  indexList* list = malloc(sizeof(indexList) * number_of_urls);
  int i = 0;
  char string[MAX_LENGTH_LINE];
  FILE* filename = fopen("pagerankList.txt", "r");
  while (fgets(string, MAX_LENGTH_LINE, filename) != NULL) {
    strcpy(list[i].URL, strtok(string, ", "));
    strtok(NULL, ", ");
    list[i].searchPR = atof(strtok(NULL, ", "));
    i++;
  }
  fclose(filename);
  return list;
}

void showInvertedIndex(indexList* list, int number_of_urls) {
  int i = 0;
  while (i < number_of_urls && i < MAX_LINE_RESULT) {
    if (list[i].searchPR >= 1.0) {
      printf("%s\n", list[i].URL);
    }
    i++;
  }
}

indexList* invertedIndexSorted(indexList* list, int number_of_urls) {
  indexList tmp;
  int edited = 1;
  while (edited == 1) {
    edited = 0;
    for (int i = 1; i < number_of_urls; i++) {
      if (list[i - 1].searchPR < list[i].searchPR) {
        edited = 1;
        tmp.searchPR = list[i - 1].searchPR;
        list[i - 1].searchPR = list[i].searchPR;
        list[i].searchPR = tmp.searchPR;
        strcpy(tmp.URL, list[i - 1].URL);
        strcpy(list[i - 1].URL, list[i].URL);
        strcpy(list[i].URL, tmp.URL);
      }
    }
  }
  return list;
}