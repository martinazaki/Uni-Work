#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

struct node {
    struct node *next;
    int          data;
};

int get_middle(struct node *head);
int length(struct node *head);
struct node *strings_to_list(int len, char *strings[]);

int main(int argc, char *argv[]) {
    // create linked list from command line arguments
    struct node *head = strings_to_list(argc - 1, &argv[1]);

    int result = get_middle(head);
    printf("%d\n", result);

    return 0;
}

// Return middle element of a linked list
// if list contains [6,7,8,9,10]  8 is returned
// if a list has even number of elements, first of middle two elements returned
// if list contains [1,2,3,4] 2 is returned
// list can not be empty
int get_middle(struct node *head) {
    assert(head != NULL);
    int len = length(head);
    int middle = (len - 1)/2;

    int i = 0;
    struct node *n = head;
    while (i < middle) {
        i = i + 1;
        n = n->next;
    }
    return n->data;
}

// Return length of a linked list.
int length(struct node *head) {
    int len = 0;
    struct node *n = head;
    while (n != NULL) {
        len = len + 1;
        n = n->next;
    }
    return len;
}


// create linked list from array of strings
struct node *strings_to_list(int len, char *strings[]) {
    struct node *head = NULL;
    for (int i = len - 1; i >= 0; i = i - 1) {
        struct node *n = malloc(sizeof (struct node));
        assert(n != NULL);
        n->next = head;
        n->data = atoi(strings[i]);
        head = n;
    }
    return head;
}
