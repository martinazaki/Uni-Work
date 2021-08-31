
#include "list.h"

#define true 1
void appendValue(List diffList, int append_value);

List listSetDifference(List l1, List l2) {
	// Creates new node to store difference in
	List diffList = newList();

	Node crr1 = l1->head;
	Node crr2 = l2->head;

	int inBoth = false;
	int leave = 0;

	while (crr1 != NULL) {
		leave = 0;
		inBoth = false;
		crr2 = l2->head;

		while (crr2 != NULL && leave == 0) {
			if (crr1->value == crr2->value) {
				inBoth = true;
				leave = 1;
			}
			crr2 = crr2->next;

		}

		if (inBoth == false && crr1 != NULL) {
			appendValue(diffList, crr1->value);

		}
		crr1 = crr1->next;

	}

	return diffList;
}


void appendValue(List diffList, int append_value) {
	Node new_node = newNode(append_value);
	if (diffList->head == NULL) {
		diffList->head = new_node;

	} else {
		Node crr_node = diffList->head;
		while (crr_node != NULL) {
			if (crr_node->next == NULL) {
				crr_node->next = new_node;
				new_node->next = NULL;

			}
			crr_node = crr_node->next;

		}


	}

}