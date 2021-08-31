#include "tree.h"

int max(int a, int b);
int height(Tree t);
Tree depthAdjustedTree(Tree fullTree, int totalDepth, Tree newTree, int depth);

Tree TreeCopy(Tree t, int depth) {
	if (depth < 0) {
		return NULL;
	}
	
	struct node *new = calloc(1, sizeof(struct node));
	int totalDepth = max(height(t->left), height(t->right));
	return depthAdjustedTree(t, totalDepth, new, depth);
}

int max(int a, int b) {
	if (a > b) {
		return a;
	} else {
		return b;
	}
}

int height(Tree t) {
	if (t == NULL) {
		return 0;
	} else {
		return 1 + max(height(t->left), height(t->right));
	}
}

Tree depthAdjustedTree(Tree fullTree, int totalDepth, Tree newTree, int depth) {
	static int currentDepth = 0;

	if (fullTree == NULL || currentDepth > totalDepth || currentDepth > depth) {
		return NULL;
	}

	if (depth >= currentDepth) {
		newTree->value = fullTree->value;
		if (depth != currentDepth) {
			currentDepth++;
			newTree->left = calloc(1, sizeof(struct node));
			newTree->left = depthAdjustedTree(fullTree->left, depth, newTree->left, totalDepth);
			newTree->right = calloc(1, sizeof(struct node));
			newTree->right = depthAdjustedTree(fullTree->right, depth, newTree->right, totalDepth);
			currentDepth--;
		} 
	}
	return newTree;
}

