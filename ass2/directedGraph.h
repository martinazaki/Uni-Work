// Lab Work
// Added to by Martina Zaki, z5264835

#ifndef DIRECTED_GRAPH_H
#define DIRECTED_GRAPH_H

#include <stdbool.h>

typedef struct GraphRep *Graph;

typedef int Vertex;

typedef struct Edge {
   Vertex v;
   Vertex u;
} Edge;

Graph newGraph(int);
void  insertEdge(Graph, Edge);
void  removeEdge(Graph, Edge);
bool  adjacent(Graph, Vertex, Vertex);
void  showGraph(Graph);
void  freeGraph(Graph);
int outDegree(Graph, Vertex);

#endif