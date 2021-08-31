// Written by Martina Zaki, z5264835

#include "invertedIndex.h"

#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void myPrintedIndexFunction(InvertedIndexBST tree);
void printWordAndFileList(FILE *f, InvertedIndexBST tree);
void printTree(InvertedIndexBST tree, FILE f);

char **getStringArrayOfItems(char *fileName);

int isFile(char *filename);
int isFileInListAlready(char *str, FileList fileList);

FileList createListNode(char *str);
FileList updateList(char *str, InvertedIndexBST node);
InvertedIndexBST upsertNodeInTree(char *word, char *file, InvertedIndexBST tree);
InvertedIndexBST createTreeNode(char *key, char *file);
InvertedIndexBST generateInvertedIndex(char *collectionFilename);

TfIdfList createTfIdfList(char *listName, double tfidfSum);
InvertedIndexBST findNodeInTree(char *searchWord, InvertedIndexBST tree);
TfIdfList traverseTreeWithSearch(TfIdfList head, InvertedIndexBST tree, char *searchWord, int D);

double calculateTF(char *searchWord, char *fileName);
double calculateIDF(char *searchWord, FileList documentList, int D);
int getOccurenceCount(char *searchWord, char *fileName);
int getWordCount(char *searchWord, char *fileName);

/**
 * Normalises a given string. See the spec for details. Note: you should
 * modify the given string - do not create a copy of it.
 */
char *normaliseWord(char *str) {
  int i = 0;
  int wordLength = strlen(str) - 1;
  char lastC = str[wordLength];

  while (i <= wordLength) {
    str[i] = tolower(str[i]);
    i++;
  }

  if (lastC == '.' || lastC == ',' || lastC == ';' || lastC == '?') {
    str[strlen(str) - 1] = 0;
  }
  return str;
}

/**
 * This function opens the collection file with the given name, and then
 * generates an inverted index from those files listed in the collection
 * file,  as  discussed  in  the spec. It returns the generated inverted
 * index.
 */

InvertedIndexBST generateInvertedIndex(char *collectionFilename) {
  InvertedIndexBST tree = NULL;
  char **files = getStringArrayOfItems(collectionFilename);
  for (size_t i = 0; (i < strcmp(files[i], "")) != 0; i++) {
    char **words = getStringArrayOfItems(files[i]);
    for (size_t j = 0; strcmp(words[j], "") != 0; j++) {
      normaliseWord(words[j]);
      tree = upsertNodeInTree(words[j], files[i], tree);
    }
  }
  //myPrintedIndexFunction(tree);
  return tree;
}

/**
 * This function returns an array of words it finds the given file.
 * We can used this twice for both the file name and the words
 * 
 */

char **getStringArrayOfItems(char *fileName) {
  FILE *file = fopen(fileName, "r");
  if (file == NULL) {
    printf("No such file.");
  }

  char **files = malloc(1000 * sizeof(1000));
  int i = 0;
  files[i] = malloc(100 * sizeof(1000));
  while (fscanf(file, "%s", files[i]) != EOF) {
    files[++i] = malloc(100 * sizeof(1000));
  }
  fclose(file);
  return files;
}

/**
 * This function handles inserting a node into the tree, as well as
 * updating an existing node's list.
 * 
 */

InvertedIndexBST upsertNodeInTree(char *word, char *file, InvertedIndexBST tree) {
  if (tree == NULL) {
    return createTreeNode(word, file);
  } else {
    int comp = strcmp(word, tree->word);
    if (comp < 0) {
      tree->left = upsertNodeInTree(word, file, tree->left);
    } else if (comp > 0) {
      tree->right = upsertNodeInTree(word, file, tree->right);
    } else if (comp == 0) {
      tree->fileList = updateList(file, tree);
    } else {
      return NULL;
    }
  }
  return tree;
}

/**
 * This function handles creating a fresh TreeNode
 */

InvertedIndexBST createTreeNode(char *key, char *file) {
  InvertedIndexBST node = malloc(sizeof(*node));
  node->word = key;
  node->fileList = createListNode(file);
  node->left = NULL;
  node->right = NULL;
  return node;
}

/**
 * This function handles creating a fresh ListNode
 */

FileList createListNode(char *str) {
  FileList newList = malloc(sizeof(*newList));
  newList->filename = str;
  newList->tf = 0.0;
  newList->next = NULL;
  return newList;
}

/**
 * This function handles updating a Node's list, if the list is
 * empty we create a new node and return that, otherwise we 
 * insert it in alphabetical order. We do this by iterating through
 * the list and placing the word where it belongs.
 */

FileList updateList(char *str, InvertedIndexBST node) {
  FileList head = node->fileList;
  FileList previous, current;
  FileList newList = createListNode(str);

  if (head == NULL) {
    return newList;
  } else {
    if (isFileInListAlready(str, head) == 0) {
      if (strcmp(head->filename, str) >= 0) {
        newList->next = head;
        head = newList;
      } else {
        previous = head; /* trailing pointer */
        current = head->next;
        while ((current != NULL) && strcmp(current->filename, str) < 0) {
          previous = current;
          current = current->next;
        }
        newList->next = previous->next;
        previous->next = newList;
      }
    }
  }
  return head;
}

/**
 * This function checks to see if the node is already 
 * in the list by comparing the filename word to the 
 * node's filename
 */

int isFileInListAlready(char *str, FileList fileList) {
  FileList curr = fileList;
  while (curr != NULL) {
    if (strcmp(str, curr->filename) == 0) {
      return 1;
    }
    curr = curr->next;
  }
  return 0;
}

/**
 * Outputs  the  given inverted index to a file named invertedIndex.txt.
 * The output should contain one line per word, with the  words  ordered
 * alphabetically  in ascending order. Each list of filenames for a word
 * should be ordered alphabetically in ascending order.
*/

void printInvertedIndex(InvertedIndexBST tree) {
  FILE *f = fopen("invertedIndex.txt", "w");
  if (f == NULL) {
    printf("Error opening file!\n");
    exit(1);
  }
  printWordAndFileList(f, tree);
  fclose(f);
}

/**
 * This is a helper function thats used to recursively print
 * the contents of the tree to a given file f.
 */

void printWordAndFileList(FILE *f, InvertedIndexBST tree) {
  if (tree != NULL) {
    printWordAndFileList(f, tree->left);
    FileList curr = tree->fileList;
    fprintf(f, "%s ", tree->word);
    while (curr != NULL) {
      fprintf(f, "%s ", curr->filename);
      curr = curr->next;
    }
    fprintf(f, "\n");
    printWordAndFileList(f, tree->right);
  }
}

/**
 * This is a helper function thats used to recursively print
 * the contents of the tree to the console for debugging.
 */

void myPrintedIndexFunction(InvertedIndexBST tree) {
  if (tree != NULL) {
    myPrintedIndexFunction(tree->left);
    FileList curr = tree->fileList;
    printf("%s ", tree->word);
    while (curr != NULL) {
      printf("%s ", curr->filename);
      curr = curr->next;
    }
    printf("\n");
    myPrintedIndexFunction(tree->right);
  }
}

// Functions for Part-2

/**
 * Returns  an  ordered list where each node contains a filename and the
 * corresponding tf-idf value for a given searchWord. You only  need  to
 * include documents (files) that contain the given searchWord. The list
 * must  be  in  descending order of tf-idf value. If there are multiple
 * files with same  tf-idf  value,  order  them  by  their  filename  in
 * ascending order.
*/
TfIdfList calculateTfIdf(InvertedIndexBST tree, char *searchWord, int D) {
  TfIdfList finalList = NULL;

  // Get the word from the tree
  InvertedIndexBST wordNode = findNodeInTree(searchWord, tree);
  if (wordNode != NULL) {
    FileList document = wordNode->fileList;
    // Iterate through the word's file list to see the documents it sits in.
    // For each document, we want to calculate the tf, idf and the tfidf
    while (document != NULL) {
      double calc_tf = calculateTF(searchWord, document->filename);
      double calc_idf = calculateIDF(searchWord, wordNode->fileList, D);
      double tfidf = calc_tf * calc_idf;

      // We then create a node with the document name, and its values.
      TfIdfList node = createTfIdfList(document->filename, tfidf);
      TfIdfList previous, current;

      // Insert them as sorted. Need to also implement matching values sorting.
      if (finalList == NULL) {
        finalList = node;
      } else {
        if (node->tfIdfSum > finalList->tfIdfSum) {
          node->next = finalList;
          finalList = node;
        } else {
          previous = finalList; /* trailing pointer */
          current = finalList->next;
          while ((current != NULL) && node->tfIdfSum > finalList->tfIdfSum) {
            previous = current;
            current = current->next;
          }
          node->next = previous->next;
          previous->next = node;
        }
      }
      document = document->next;
    }
  } else {
    printf("Word Not Found in Tree\n");
    return NULL;
  }
  return finalList;
}

/*
   A function that takes in a search word and a document, and searches for all the occurences of that word in the document. It then divdes by the total word
   count.
  */

double calculateTF(char *searchWord, char *fileName) {
  int occurences = 0;
  int wordCount = 0;
  char **words = getStringArrayOfItems(fileName);
  for (size_t i = 0; (i < strcmp(words[i], "")) != 0; i++) {
    if (strcmp(searchWord, normaliseWord(words[i])) == 0) {
      occurences++;
    }
    wordCount++;
  }
  return (double)occurences / (double)wordCount;
}

/**
 * Function for getting the idf, we need to count how many times the word    
 * appears across all the documents, based our tree structure this is just the  * length of the list.
*/

double calculateIDF(char *searchWord, FileList documentList, int D) {
  int listLength = 0;

  while (documentList != NULL) {
    listLength++;
    documentList = documentList->next;
  }
  return log10(D / (double)listLength);
}

/**
 * Function used to find a node in the tree, once it find its it returns its
 * filelist as a TfIdfList, this used the helper function called 
 * createTfIdfListFromFileList to do so
 * 
*/

InvertedIndexBST findNodeInTree(char *searchWord, InvertedIndexBST tree) {
  if (tree == NULL) {
    return NULL;
  } else {
    int comp = strcmp(searchWord, tree->word);
    if (comp < 0) {
      return findNodeInTree(searchWord, tree->left);
    } else if (comp > 0) {
      return findNodeInTree(searchWord, tree->right);
    } else if (comp == 0) {
      return tree;
    } else {
      return NULL;
    }
  }
  return NULL;
}

/**
 * This function handles creating a fresh createTfIdfList Node
 */

TfIdfList createTfIdfList(char *listName, double tfidfSum) {
  TfIdfList node = malloc(sizeof(*node));
  node->filename = listName;
  node->tfIdfSum = tfidfSum;
  node->next = NULL;
  return node;
}

/**
 * Returns  an  ordered list where each node contains a filename and the
 * summation of tf-idf values of all the matching search words for  that
 * file.  You only need to include documents (files) that contain one or
 * more of the given search words. The list must be in descending  order
 * of summation of tf-idf values (tfIdfSum). If there are multiple files
 * with  the  same tf-idf sum, order them by their filename in ascending
 * order.
 */
TfIdfList retrieve(InvertedIndexBST tree, char *searchWords[], int D) {
  return NULL;
}
