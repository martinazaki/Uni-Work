// Written by Martina Zaki, z5264835

// mergeOrdered.c ... implementation of mergeOrdered function

#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "list.h"

void listInsert(List list, int v);
/* 
    You will submit only this one file.

    Implement the function "mergeOrdered" below. Read the exam paper for a
    detailed specification and description of your task.  

    - DO NOT modify the code in any other files. 
    - You can add static helper functions to this file.  
    - DO NOT add a "main" function to this file. 
*/

List mergeOrdered(List list1, List list2) {
  // Creates new list to store merged one in
  List mergedList = newList();

  // Create a node that points to the lists to create another variable
  struct _node *curr1 = list1->first;
  struct _node *curr2 = list2->first;

  // Going through list
  while (curr1 != NULL || curr2 != NULL) {
    if (curr1 == NULL) {
      listInsert(mergedList, curr2->value);
      curr2 = curr2->next;
    } else if (curr2 == NULL) {
      listInsert(mergedList, curr1->value);
      curr1 = curr1->next;
    } else if (curr1->value <= curr2->value) {
      listInsert(mergedList, curr1->value);
      curr1 = curr1->next;
    } else {
      listInsert(mergedList, curr2->value);
      curr2 = curr2->next;
    }
  }
  return mergedList;
}

void listInsert(List list, int v) {
  struct _node *new;

  assert(list != NULL);
  new = newNode(v);
  if (list->first == NULL)
    list->first = list->last = new;
  else {
    list->last->next = new;
    list->last = new;
  }
}
