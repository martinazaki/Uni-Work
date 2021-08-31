// Written by Martina Zaki, z5264835

#ifndef SEARCH_PAGERANK_H
#define SEARCH_PAGERANK_H

typedef struct indexList {
  char URL[MAX_LENGTH_URL];
  float searchPR;
} indexList;

int numberOfURLS();

indexList* invertedIndexDetails(int number_of_urls);

void showInvertedIndex(indexList* list, int number_of_urls);

indexList* invertedIndexSorted(indexList* list, int number_of_urls);

#endif