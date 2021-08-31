#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

struct node {
    struct node *next;
    int          data;
};

int intersection_size(struct node *head1, struct node *head2);
int member(int i, struct node *head);
struct node *strings_to_list(int len, char *strings[]);

// DO NOT CHANGE THIS MAIN FUNCTION
int main(int argc, char *argv[]) {
    // create two linked lists from command line arguments
    int dash_arg = argc - 1;
    while (dash_arg > 0 && strcmp(argv[dash_arg], "-") != 0) {
        dash_arg = dash_arg - 1;
    }
    struct node *head1 = strings_to_list(dash_arg - 1, &argv[1]);
    struct node *head2 = strings_to_list(argc - dash_arg - 1, &argv[dash_arg + 1]);

    int result = intersection_size(head1, head2);
    printf("%d\n", result);

    return 0;
}

// return the number of values which occur in both linked lists
// no value is repeated in either list
int intersection_size(struct node *head1, struct node *head2) {
    int num_both = 0;
    struct node *p = head1;
    while (p != NULL) {
        if (member(p->data, head2)) {
            num_both = num_both + 1;
        }
        p = p->next;
    }
    return num_both;
}

// return 1 if i occurs in list, 0 otherwise
int member(int i, struct node *head) {
    struct node *p = head;
    while (p != NULL) {
        if (p->data == i) {
            return 1;
        }
        p = p->next;
    }
    return 0;
}


// DO NOT CHANGE THIS FUNCTION
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

