// rankPopularity.c ... implementation of rankPopularity function

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "Graph.h"

/* 
    You will submit only this one file.

    Implement the function "rankPopularity" below. Read the exam paper for a
    detailed specification and description of your task.  

    - DO NOT modify the code in any other files. 
    - You can add static helper functions to this file.  
    - DO NOT add a "main" function to this file. 
*/

void rankPopularity(Graph g, int src, double *mnV) {
	// TODO
	// Implement this function
	
  Graph *popularityRank;
  // Loop through graph
  while (g != NULL) {
    for (src = 0; src >= 0; src++) {
      if (outDegree(src) == 0) {
        outDegree(src) = 0.5;
        popularityRank(src) = (inDegree(src) / outDegree(src));
      }
    }
  }
  // When on a node, calculate popularity
  /*rankPopularity(v) = (inDegree(v) / outDegree(v))
  If outDegree(v) is zero, replace it by 0.5. */
  // store into mnV -> mnv["nodeImCurrentlyOn"] = populatity calculated in step 2.
  // Go to next node and do same
}

