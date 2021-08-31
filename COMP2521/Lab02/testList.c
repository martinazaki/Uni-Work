// testList.c - testing DLList data type
// Written by John Shepherd, March 2013

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#include "DLList.h"

#define False 0
#define True 1

int main (void)
{
DLList myList = getDLList (stdin);
putDLList (stdout, myList);
assert (validDLList (myList));

// TODO: more tests needed here

// TESTS FOR DLLISTBEFORE FUNCTION
printf("Testing Phase 1 - DLListBefore Function\n");
printf("\n");
   
    //--------------------------------------------------------------------------
   
    // Test 1 for when current is head
    printf("---> Testing DLListBefore Function when current is head\n");

// Switch current to head
DLListMoveTo(myList, 1);

char* test1 = "Test 1 for edge cases\n";
DLListBefore(myList, test1);

assert (validDLList(myList));
printf("------> DLListBefore function works normally when current is\n");
printf("------> head. Edge case 1 complete for DLListBefore function\n");
printf("\n");

//--------------------------------------------------------------------------

// Test 1.1 for when current is tail
printf("---> Testing DLListBefore Function when current is tail\n");

// Switch current to tail first
DLListMoveTo(myList, DLListLength(myList));

char* test1_1 = "Test 1.1 for edge cases\n";
DLListBefore(myList, test1_1);

assert (validDLList(myList));
printf("------> DLListBefore function works normally when current is\n");
printf("------> tail. Edge case 1.1 complete for DLListBefore function\n");
printf("\n");

//--------------------------------------------------------------------------

// Test 1.2 for when current is not tail or head (normal cases)
printf("---> Testing DLListBefore Function in normal cases\n");

// Switch current to head
DLListMoveTo(myList, 1);

// Add more nodes
char *data1 = "minus";
char *data2 = "why";
char *data3 = "UNSW is not bad";
DLListBefore(myList, data1);
DLListBefore(myList, data2);
DLListBefore(myList, data3);


// Switch current a node between two nodes
DLListMoveTo(myList, 2);


char* test1_2 = "Test 1.2 for normal cases\n";
DLListBefore(myList, test1_2);

assert (validDLList(myList));
printf("------> DLListBefore function works normally when current is\n");
printf("------> tail. Normal case 1.2 complete for DLListBefore function\n");


//--------------------------------------------------------------------------
printf("\n");

// TEST FOR DLLISTAFTER FUNCTION
printf("Testing Phase 2 - DLListAfter Function\n");

// Switch current to head
DLListMoveTo(myList, 1);

// Test 2 for when current is head
char* test2 = "Test 2 for edge cases\n";
printf("---> Testing DLListAfter Function when current is head\n");
DLListAfter(myList, test2);

assert (validDLList(myList));
    printf("------> DLListAfter function works normally when current is\n");
printf("------> head.  Edge case 1 complete for DLListAfter function\n");
printf("\n");

//--------------------------------------------------------------------------

// Test 2.1 for when current is tail
printf("---> Testing DLListAfter Function when current is tail\n");

// Switch current to tail first
DLListMoveTo(myList, DLListLength(myList));

char* test2_1 = "Test 2.1 for edge cases\n";
printf("---> Testing DLListAfter Function when current is tail\n");
DLListBefore(myList, test2_1);

assert (validDLList(myList));
printf("------> DLListAfter function works normally when current is\n");
printf("------> tail. Edge case 2.1 complete for DLListAfter function\n");

//--------------------------------------------------------------------------

    // Test 2.2 for when current is not tail or head (normal cases)
printf("---> Testing DLListAfter Function in normal cases\n");

// Switch current to head
DLListMoveTo(myList, 1);

// Add more nodes
char *node1 = "Adding";
char *node2 = "why not";
char *node3 = "UNSW isnt too bad";
DLListBefore(myList, node1);
DLListBefore(myList, node2);
DLListBefore(myList, node3);


// Switch current a node between two nodes
DLListMoveTo(myList, 2);


char* test2_2 = "Test 2.2 for normal cases\n";
printf("---> Testing DLListAfter Function in normal cases\n");
DLListAfter(myList, test2_2);

assert (validDLList(myList));
printf("------> DLListAfter function works normally when current is\n");
printf("------> tail. Normal case 2.2 complete for DLListAfter function\n");

//--------------------------------------------------------------------------
printf("\n");

// TEST FOR DLLISTDELETE FUNCTION
printf("Testing Phase 3 - DLListDelete Function\n");

// Switch current to head
DLListMoveTo(myList, 1);


// Test 3 for when current is head
char* test3 = "Test 3 for edge cases\n";
printf("---> Testing DLListDelete Function when current is head\n");
DLListDelete(myList);

assert (validDLList(myList));
    printf("------> DLListDelete function works normally when current is\n");
printf("------> head. Edge case 1 complete for DLListDelete function\n");
printf("\n");

//--------------------------------------------------------------------------

// Test 3.1 for when current is tail
printf("---> Testing DLListDelete Function when current is tail\n");

// Switch current to tail first
DLListMoveTo(myList, DLListLength(myList));

printf("---> Testing DLListDelete Function when current is tail\n");
DLListDelete(myList);

assert (validDLList(myList));
printf("------> DLListDelete function works normally when current is\n");
printf("------> tail. Edge case 3.1 complete for DLListDelete function\n");

printf("\n");

//--------------------------------------------------------------------------

    // Test 3.2 for when current is not tail or head (normal cases)
printf("---> Testing DLListAfter Function in normal cases\n");

// Switch current to head
DLListMoveTo(myList, 1);

// Add more nodes
char *info1 = "Lets get";
char *info2 = "this bread ";
char *info3 = "UNSW please close corona getting serious";
DLListBefore(myList, info1);
DLListBefore(myList, info2);
DLListBefore(myList, info3);


// Switch current a node between two nodes
DLListMoveTo(myList, 2);


printf("---> Testing DLListDelete Function in normal cases\n");
DLListDelete(myList);

assert (validDLList(myList));
printf("------> DLListDelete function works normally when current is\n");
printf("------> tail.Normal case 3.2 complete for DLListDelete function\n");

   
   
   
    printf("\n");
freeDLList (myList);
return EXIT_SUCCESS;
}
