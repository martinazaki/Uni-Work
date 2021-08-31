// Written by Martina Zaki, z5264835

#ifndef PAGERANK_H
#define PAGERANK_H

#include "lengthDefinitions.h"

typedef struct PRNode {
  char url[MAX_LENGTH_URL];
  int degree;
  float rank;
} PRNode;

// return  number of URLs in file
int retrieveURLNumber();

// creates PR list
PRNode *formPRList(int nURL);

// writes PR list
int writePRList(PRNode *PRList, int number_of_url);

// creates graph data structure
Graph formGraph(PRNode *PRList, int number_of_url);

// returns  index of a URL
int findURLIndex(char *url, PRNode *PRList, int number_of_url);

// generates degree into PRList
int findOutDegree(Graph file, PRNode *PRList, int number_of_url);

// calculates pagerank into PRList
int calculatePagerank(float d, float minDifference, int maxIterations,
                      Graph file, PRNode *PRList, int number_of_url);

// sort PRList in descending order
int orderPRList(PRNode *PRList, int number_of_url;

// prints the debug information on the screen
void debug(float d, float minDifference,int maxIterations,
                    PRNode *PRList, int number_of_url);

#endif