// Written by Martina Zaki, z5264835

#include <stdio.h>
#include <stdlib.h>

#include "list.h"

#define true    1
void appendValue(List abnormalList, int append_value); 

List listGetAbnormals(List l, int threshold) {
    // Create a new linked list for the new list
    List abnormalList = newList();

    // Create a node that points to the lists to create another variable
    Node curr1 = l->first;
    
	// If list is empty 
	if (curr1 == NULL) {
		return abnormalList;

	} 
	
	int abnormal = false;

    // Loop through the list
    while (curr1->next != NULL) {
		// Checking if the previous node is empty
		if (curr1->prev == NULL) {
			curr1 = curr1->next;
			continue;
		}
        // Compare if absolute difference meets criteria
        if (abs(curr1->value - curr1->prev->value) >= threshold && abs(curr1->value - curr1->next->value) >= threshold) {
            abnormal = true;

        } else {
			abnormal = false;
		}

        if (abnormal == true) {
            appendValue(abnormalList, curr1->value);
        
        }
        curr1 = curr1->next;

    }
    // Return list containing abnormal values
	return abnormalList;

}

void appendValue(List abnormalList, int append_value) {
	// Count for the size
    abnormalList->size++;
	
    // Appending new node
	Node new_node = newNode(append_value);
	abnormalList->last = new_node;

	if (abnormalList->first == NULL) {
		abnormalList->first = new_node;

	} 
    
    else {
		Node curr_node = abnormalList->first;
		while (curr_node != NULL) {
			if (curr_node->next == NULL) {
				new_node->prev = curr_node;
				new_node->next = NULL;
				curr_node->next = new_node;
				break;

			}
			curr_node = curr_node->next;

		}

	}

}
