
#include <stdlib.h>

#include "BSTree.h"

int numberNodes(BSTree t);

int BSTreeGetKth(BSTree t, int k) {
	if (k == numberNodes(t->left)) {
		return t->value;
	} else if (k < numberNodes(t->left)) {
		return BSTreeGetKth(t->left, k);
	} else {
		k = k - numberNodes(t->left) - 1;
		return BSTreeGetKth(t->right, k);
	}
}

int numberNodes(BSTree t) {
	if (t == NULL) {
		return 0;
	} else {
		return 1 + numberNodes(t->left) + numberNodes(t->right);
	}
}


