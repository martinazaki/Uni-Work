// Written by Martina Zaki, z5264835

#include "pagerank.h"

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "Graph.h"
#include "lengthDefinitions.h"

int main(int argc, char *argv[]) {
  assert(argc == 4);
  float d = atof(argv[1]);
  float minDifferece = atof(argv[2]);
  int maxIterations = atoi(argv[3]);
  int number_of_url = retrieveURLNumber();

  PRNode *PRList = formPRList(number_of_url);
  Graph web = createGraph(PRList, number_of_url);
  findOutDegree(web, PRList, number_of_url);
  calculatePagerank(d, minDifferece, maxIterations, web, PRList, number_of_url);
  orderPRList(PRList, number_of_url);
  writePRList(PRList, number_of_url);
  freeGraph(web);
  free(PRList);
  return EXIT_SUCCESS;
}

int retrieveURLNumber() {
  int number_of_url = 0;
  char url[MAX_LENGTH_URL];
  FILE *filename = fopen("collection.txt", "r");
  while (fscanf(filename, "%s", url) != EOF) {
    number_of_url++;
  }
  fclose(filename);
  return number_of_url;
}

PRNode *formPRList(int number_of_url) {
  char url[MAX_LENGTH_URL];
  PRNode *PRList = malloc(sizeof(PRNode) * number_of_url);
  assert(PRList != NULL);
  FILE *filename = fopen("collection.txt", "r");

  int i = 0;
  while (fscanf(filename, "%s", url) != EOF) {
    strcpy(PRList[i].url, url);
    PRList[i].degree = 0;
    PRList[i].rank = 0;
    i++;
  }
  fclose(filename);
  return PRList;
}

int writePRList(PRNode *PRList, int number_of_url) {
  FILE *filename = fopen("pagerankList.txt", "w");
  for (int i = 0; i < number_of_url; i++) {
    fprintf(filename, "%s, %d, %.7f\n",
            PRList[i].url, PRList[i].degree, PRList[i].rank);
  }
  fclose(filename);
  return 1;
}

Graph formGraph(PRNode *PRList, int number_of_url) {
  Graph newG = newGraph(number_of_url);
  char file[MAX_LENGTH_URL + 4];
  char extension[] = ".txt";
  FILE *pageDetails;
  int number_of_hash;  // hash symbol encountered
  char url[MAX_LENGTH_URL];
  Edge link;

  for (int i = 0; i < number_of_url; i++) {
    // generate the file name
    strcpy(file, PRList[i].url);
    strcat(file, extension);
    // printf("now reading file %s\n", file);

    pageDetails = fopen(file, "r");
    number_of_hash = 0;
    while (fscanf(pageDetails, "%s", url) != EOF) {
      if (url[0] == '#') {
        number_of_hash++;
        if (number_of_hash == 1) {
          fscanf(pageDetails, "%s", url);
        }
        if (number_of_hash == 2) {
          break;
        }
      } else {
        // printf("URLs included: %s\n", url);

        link.v = findURLIndex(PRList[i].url, PRList, number_of_url);
        link.u = findURLIndex(url, PRList, number_of_url);
        insertEdge(newG, link);
      }
    }
    fclose(pageDetails);
  }
  return newG;
}

int findURLIndex(char *url, PRNode *PRList, int number_of_url) {
  for (int i = 0; i < number_of_url; i++) {
    if (strcmp(PRList[i].url, url) == 0) {
      break;
    }
  }
  return i;
}

int findOutDegree(Graph file, PRNode *PRList, int number_of_url) {
  for (int i = 0; i < number_of_url; i++) {
    PRList[i].degree = outDegree(file, i);
  }
  return 1;
}

int calculatePagerank(float d, float minDifference, int maxIterations,
                      Graph file, PRNode *PRList, int number_of_url) {
  float *newPR = malloc(sizeof(float) * number_of_url);
  assert(newPR != NULL);
  float tempPR = 0;
  int iteration;
  float diff;
  float diffPR;

  // initialises PR
  for (int i = 0; i < number_of_url; i++) {
    PRList[i].rank = 1.0 / number_of_url;
    newPR[i] = 1.0 / number_of_url;
  }

  // calculate PR
  iteration = 0;
  diffPR = minDifference;
  while (iteration < maxIteration && diff >= diffPR) {
    for (int i = 0; i < N; i++) {
      float tempPR = 0;
      for (int j = 0; j < N; j++) {
        if (adjacent(file, j, i)) {
          tempPR += PRList[j].rank / PRList[j].degree;
          if (tempPR[i]->outDegree == 0) {
            tempPR[i]->outDegree = 0.5;
          }
        }
      }
      newPR[i] = (1.0 - d) / N + d * tempPR;
    }

    // calculate diff
    diffPR = 0;
    for (i = 0; i < number_of_url; i++) {
      diff = PRList[i].rank - newPR[i];
      if (diff < 0) {
        diff = -diff;
      }
      totalDiff += diff;
    }

    for (i = 0; i < number_of_url; i++) {
      PRList[i].rank = newPR[i];
    }
    iteration++;
  }

  free(newPR);
  return 1;
}

int orderPRList(PRNode *PRList, int number_of_url) {
  int swap = 1;
  PRNode tmp;
  while (swap == 1) {
    swap = 0;
    for (int i = 1; i < number_of_url; i++) {
      if (PRList[i - 1].rank < PRList[i].rank) {
        swap = 1;

        strcpy(tmp.url, PRList[i].url);
        tmp.degree = PRList[i].degree;
        tmp.rank = PRList[i].rank;
        strcpy(PRList[i].url, PRList[i - 1].url);
        PRList[i].degree = PRList[i - 1].degree;
        PRList[i].rank = PRList[i - 1].rank;
        strcpy(PRList[i - 1].url, tmp.url);
        PRList[i - 1].degree = tmp.degree;
        PRList[i - 1].rank = tmp.rank;
      }
    }
  }
  return 1;
}

void debug(float d, float minDifference,
           int maxIterations, PRNode *PRList, int number_of_url) {
  int i;
  float sum = 0;
  printf("Input parameters:\n");
  printf("d = %.7f\n", d);
  printf("minDifferece = %.7f\n", minDifferece);
  printf("maxIterations = %d\n", maxIterations);
  printf("Number of URLs: %d\n", number_of_url);
  printf("PRList:\n");
  for (i = 0; i < number_of_url; i++) {
    printf("%s, %d, %.7f\n", PRList[i].url,
           PRList[i].degree, PRList[i].rank);
  }
  for (i = 0; i < number_of_url; i++) {
    sum += PRList[i].rank;
  }
  printf("The sum of pagerank is: %f\n", sum);
}