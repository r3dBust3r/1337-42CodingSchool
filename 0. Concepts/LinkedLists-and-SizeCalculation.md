# Linked Lists in C

A **linked list** is a **dynamic data structure** made up of a sequence of **nodes**, where each node contains:

1. Some **data**
2. A **pointer** to the next node in the list

Unlike arrays, linked lists:

* Do **not** store elements in contiguous memory.
* Can **grow or shrink** at runtime.
* Require **dynamic memory allocation** (`malloc`, `free`).

#### Basic Structure

A simple **singly linked list node** looks like this:

```c
struct Node
{
    int data;            // data stored in the node
    struct Node *next;   // pointer to the next node
};
```

You can also use `typedef` for convenience:

```c
typedef struct Node
{
    int data;
    struct Node *next;
} Node;
```

#### How to Calculate the Size of a Struct

**Using the `sizeof` Operator**

```c
#include <stdio.h>

struct Example
{
    char a;     // 1 byte
    int b;      // 4 bytes
    char c;     // 1 byte
};

int main()
{
    printf("Size of struct: %zu\n", sizeof(struct Example)); // Size of struct: 12
    return 0;
}
```

`sizeof(struct Example)` automatically returns the total size **in bytes**, including **padding** added by the compiler.

**Manual Calculation (with Padding)**

- Step 1: Look at individual sizes

| Member | Type | Size (bytes) |
| ------ | ---- | ------------ |
| a      | char | 1            |
| b      | int  | 4            |
| c      | char | 1            |

- Step 2: Consider **alignment and padding**

Most systems align data according to the **largest member’s alignment** (here: 4 bytes for `int`).

Memory layout (on a typical 32-bit or 64-bit system):

| Byte Offset | Data      | Notes                                   |
| ----------- | --------- | --------------------------------------- |
| 0           | `a`       | 1 byte                                  |
| 1 -> 3      | *padding* | Added so that `b` starts at offset 4    |
| 4 -> 7      | `b`       | 4 bytes                                 |
| 8           | `c`       | 1 byte                                  |
| 9 -> 11     | *padding* | Added so struct ends on 4-byte boundary |

**Total size = 12 bytes**

- **Why Padding Happens**

Padding ensures that data members are **aligned in memory** according to their natural size,
this improves CPU performance on most architectures.

- **Controlling Padding**

If you want to avoid or control padding:

* Use **pragma directives** or **attributes** (depends on compiler):

```c
#pragma pack(1)
struct Packed
{
    char a;
    int b;
    char c;
};
#pragma pack()
```

Now the struct will be packed tightly, with **no padding**:

```
a (1) + b (4) + c (1) = 6 bytes
```

But this can reduce performance on some CPUs and is not always recommended.

- Summary

| Concept               | Explanation                                       |
| --------------------- | ------------------------------------------------- |
| **`sizeof` operator** | Gives total size including padding                |
| **Padding**           | Extra bytes added for alignment                   |
| **Alignment**         | Members start at addresses multiple of their size |
| **`#pragma pack`**    | Can disable padding                               |


#### Creating a Simple Linked List

Let’s manually create a linked list of three nodes:
`10 → 20 → 30 → NULL`

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    int data;
    struct Node *next;
} l_lst;

int main()
{
    // Allocate memory for 3 nodes
    l_lst *nd1 = (l_lst *)malloc(sizeof(l_lst));
    l_lst *nd2 = (l_lst *)malloc(sizeof(l_lst));
    l_lst *nd3 = (l_lst *)malloc(sizeof(l_lst));

    // Assign data and links
    nd1->data = 100;
    nd1->next = nd2;

    nd2->data = 200;
    nd2->next = nd3;

    nd3->data = 300;
    nd3->next = NULL;

    // Traverse and print
    l_lst *temp = nd1;
    while (temp)
    {
        printf("[%d]->", temp->data);
        temp = temp->next;
    }

    printf("[NULL]\n");

    free(nd1);
    free(nd2);
    free(nd3);
    return 0;

	/*
		OUTPUTS: [100]->[200]->[300]->[NULL]
	*/
}
```

#### Traversing a Linked List

You use a pointer (often called `temp` or `current`) to walk through nodes:

```c
void print_list(l_lst *head)
{
    l_lst *temp = head;
    while (temp) {
        printf("[%d]->", temp->data);
        temp = temp->next;
    }
    printf("[NULL]\n");
}
```

#### Inserting Nodes
##### Insert at the Beginning

```c
void insert_at_beginning(l_lst **head_ref, int new_data)
{
    l_lst *new_node = (l_lst *)malloc(sizeof(l_lst));
    new_node->data = new_data;
    new_node->next = *head_ref;
    *head_ref = new_node;
}
```

##### Insert at the End

```c
void insert_at_end(l_lst **head_ref, int new_data)
{
    l_lst *new_node = (l_lst *)malloc(sizeof(l_lst));
    new_node->data = new_data;
    new_node->next = NULL;

    if (*head_ref == NULL)
	{
        *head_ref = new_node;
        return;
    }

    l_lst *temp = *head_ref;
    while (temp->next)
        temp = temp->next;

    temp->next = new_node;
}
```

##### Insert After a Given Node

```c
void insert_after(l_lst *prev_node, int new_data)
{
    if (prev_node == NULL)
	{
        printf("Previous node cannot be NULL\n");
        return;
    }
    l_lst *new_node = (l_lst *)malloc(sizeof(l_lst));
    new_node->data = new_data;
    new_node->next = prev_node->next;
    prev_node->next = new_node;
}
```

#### Deleting a Node

Delete by **value**:

```c
void delete_node(l_lst **head_ref, int key)
{
    l_lst *temp = *head_ref;
	l_lst *prev = NULL;

    // If head node holds the key
    if (temp && temp->data == key)
	{
        *head_ref = temp->next;
        free(temp);
        return;
    }

    // Search for the key
    while (temp && temp->data != key)
	{
        prev = temp;
        temp = temp->next;
    }

    // Key not found
    if (!temp)
		return;

    prev->next = temp->next;
    free(temp);
}
```

#### Freeing the Entire List

Always release memory to avoid leaks:

```c
void freeList(l_lst *head)
{
    l_lst *temp;
    while (head)
	{
        temp = head;
        head = head->next;
        free(temp);
    }
}
```

#### Calc the length of a Linked List

```c
int get_size(l_lst *hd_node) {
    int count = 0;
    while (hd_node) {
        count++;
        hd_node = hd_node->next;
    }
    return count;
}
```
