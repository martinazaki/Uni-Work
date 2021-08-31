
#include <stdlib.h>

#include "tree.h"


int numberNodes(Tree t);

bool TreeIsPerfectlyBalanced(Tree t) {
	if (t == NULL) { 
		return true;
	}
	// Difference in size between sides must be less than 1 and both subtrees must be balanced for true.
	if (abs(numberNodes(t->left) - numberNodes(t->right)) <= 1 && TreeIsPerfectlyBalanced(t->left) && TreeIsPerfectlyBalanced(t->right)) {
		return true;
	}
	return false;
}

int numberNodes(Tree t) {
	if (t == NULL) {
		return 0;
	} else {
		return 1 + numberNodes(t->left) + numberNodes(t->right);
	}
}
