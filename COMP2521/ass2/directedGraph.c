// Lab Work
// Added to by Martina Zaki, z5264835

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>
#include "Graph.h"
#include "lengthDefinitions.h"

typedef struct GraphRep {
   int  **edges; 
   int    nV;   
   int    nE;
} GraphRep;

Graph newGraph (int nV) {
   assert(nV >= 0);

   Graph new = malloc(sizeof(GraphRep));
   assert(new != NULL);
   new->nV = nV;
   new->nE = 0;

   new->edges = malloc(nV * sizeof(int *));
   assert(new->edges != NULL);
   for (int i = 0; i < nV; i++) {
      new->edges[i] = calloc(nV, sizeof(int));
      assert(new->edges[i] != NULL);
   }

   return new;
}

// check if vertex is valid in a graph
bool validV(Graph g, Vertex v) {
   return (g != NULL && v >= 0 && v < g->nV);
}

void insertEdge(Graph g, Edge e) {
   assert(g != NULL && validV(g,e.v) && validV(g,e.u));

   if (!g->edges[e.v][e.u]) {  
      g->edges[e.v][e.u] = 1;
      g->nE++;
   }
}

void removeEdge(Graph g, Edge e) {
   assert(g != NULL && validV(g,e.v) && validV(g,e.u));

   if (g->edges[e.v][e.u]) {
      g->edges[e.v][e.u] = 0;
      g->nE--;
   }
}

bool adjacent(Graph g, Vertex v, Vertex u) {
   assert(g != NULL && validV(g,v) && validV(g,u));

   return (g->edges[v][u] != 0);
}

void showGraph(Graph g) {
    assert(g != NULL);
    int i, j;

    printf("Number of vertices: %d\n", g->nV);
    printf("Number of edges: %d\n", g->nE);
    for (i = 0; i < g->nV; i++)
       for (j = 0; j < g->nV; j++)
	  if (g->edges[i][j])
	      printf("Edge %d -> %d\n", i, j);
}

void freeGraph(Graph g) {
   assert(g != NULL);

   int i;
   for (i = 0; i < g->nV; i++)
      free(g->edges[i]);
   free(g->edges);
   free(g);
}

int outDegree(Graph g, Vertex v) {
    assert(g != NULL);
    int i;
    int d = 0;
    for (i = 0; i < g->nV; i++) {
        if (g->edges[v][i]) {
            d++;
        }
    }
    return d;
}