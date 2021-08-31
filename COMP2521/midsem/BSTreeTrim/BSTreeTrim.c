// Written by Martina Zaki, z5264835

#include <stdio.h>
#include <stdlib.h>

#include "BSTree.h"

BSTree joinSubtrees(BSTree t1, BSTree t2);
BSTree TreeDeleteRoot(BSTree t);


BSTree BSTreeTrim(BSTree t, int lower, int upper) {
	if (t == NULL) {
		return t;
	}

	// Check if root node is greater than upper
	if (t->value > upper) {
		t->left = BSTreeTrim(t->left, lower, upper);
	} 
	
	// Check if root node is less than lower
	else if (t->value < lower) {
		t->right = BSTreeTrim(t->right, lower, upper);
	} 
	
	// Check if root node is between upper and lower
	else {
		t = TreeDeleteRoot(t);
		t = BSTreeTrim(t, lower, upper);
	} 
	return t;
}

// Function connect right and left subtree when you remove a root node with 2 child nodes
BSTree joinSubtrees(BSTree t1, BSTree t2) {
	if (t1 == NULL) {
		return t1;
	} 
	
	else if (t2 == NULL) {
		return t2;
	} 
	
	else {
		BSTree current = t2;
		BSTree parent_root = NULL;

		// Finds the minimum element in t2
		while (current->left != NULL) {
			parent_root = current;
			current = current->left;
		}
		
		// Condition unlinks minimum element from parent
		if (parent_root != NULL) {
			parent_root->left = current->right;
			current->right = t2;
		}
		// The minimum element is now the new root
		current->left = t1;
		return current; 
	}
}

// Function deletes root node
BSTree TreeDeleteRoot(BSTree t) {
	if (t != NULL) {
		BSTree new_root;

		if (t->left == NULL && t->right == NULL) {
			new_root = NULL;
		} 
		
		// Check if only right subtree, then makes it the new root
		else if (t->left == NULL) {    
			new_root = t->right;
		} 
		
		// Check if only left subtree, then makes it the new root
		else if (t->right == NULL) {
			new_root = t->left;
		}   
		
		// Check when t->left and t->right don't equal NULL
		else {
			new_root = joinSubtrees(t->left, t->right);
		}
		free(t);
		t = new_root;
	}
   return t;
}
