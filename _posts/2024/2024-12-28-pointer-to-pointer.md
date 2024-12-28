---
layout: post
title: Pointer to pointer
categories: [blog, leetcode]
tags: [leetcode]
---

For List related problem, we usually will not use the recursive way to solve it. For binary
search tree, we might use it. In this blog, I just want to demonstrate that we can use recursive
function to solve it by leveraging the pointer to pointer.

+ toc
{:toc}

## Non recursive way

I create

- `reverseList`: Reverse the singly linked list.
- `size`: Get the size of the list
- `compare`: Compare two lists

The basic idea is to get the size of list and split the list into two parts. We can reverse the
second half of the list and compare them one by one.

The priority of `==` is higher than `&`, so we need to add parentheses.

```cpp
class Solution {
    ListNode* reverseList(ListNode* node) {
        ListNode* head = nullptr;
        while (node) {
            auto n = node->next;
            node->next = head;
            head = node;
            node = n;
        }
        return head;
    }

    int size(ListNode* node) {
        int size = 0;
        while (node) {
            node = node->next;
            ++size;
        }
        return size;
    }

    pair<ListNode*, ListNode*> advance(ListNode* node, int step) {
        ListNode* prev = nullptr;
        while (step != 0) {
            prev = node;
            node = node->next;
            --step;
        }
        return {prev, node};
    }

    bool compare(ListNode* node1, ListNode* node2) {
        while (node1) {
            if (node1->val != node2->val) {
                return false;
            }
            node1 = node1->next;
            node2 = node2->next;
        }
        return true;
    }
public:
    bool isPalindrome(ListNode* head) {
        int size1 = size(head);
        if (size1 < 2) return true;
        auto p = advance(head, size1/2);
        p.first->next = nullptr;
        if ((size1 & 0x1) != 0) {
            p.second = p.second->next;
        }
        auto n = reverseList(p.second);
        return compare(head, n);

    }
};
```

## Recursive way

It is kind of hard to figure it out.

- When to stop the condition
- How we recursively check the nodes
- When to quit the check process

For example, we have a list of 5 nodes, [1,2,3,2,1] and the recursive function will have two inputs
 which need check.

- The first inputs will be (head, node) which node = head.
- We change the second parameter until we find that its next value is `nullptr`.
- Then we compare `head` and `node`

Then we need check `head->next` and the previous node of `node`. We will have the previous node
of `node` autotimatically when we exit next level of function and return to its caller. The hard
part is how we make sure when we return from the function, `head` is updated to its next value.

The answer is pointer to pointer. We can pass `**head` to the function and we can update it by

```cpp
*head = (*head)->next;
```

The next tricky part is when we checked `3`, we don't have to check, even the function will then
return to `2` and `1`. We have entered the function from  the beginning.

We have to skip the check. Here I assigned the `head` to a `nullptr` to signal that we can safely
skip current check.


```cpp
class Solution {
    bool isPalindromeHelper(ListNode** head, ListNode* node) {
        if (!node) return true;
        if (!node->next) {
            // tail node
            if (node->val != (*head)->val) return false;
            *head = (*head)->next;
            return true;
        } else {
            auto v = isPalindromeHelper(head, node->next);
            if (!v) return false;
            if (*head == nullptr) return true;
            if ((*head)->val != node->val) return false;
            if (*head == node) *head = nullptr;
            else if ((*head)->next == node) *head = nullptr;
            else *head = (*head)->next;
            return true;
        }
    }
public:
    bool isPalindrome(ListNode* head) {
        return isPalindromeHelper(&head, head);
    }
};
```

## Conclusion

Sometimes it is amazing to have the ability to control the memory level access like in cpp instead
of python. You can have more granularity of control.

## Reference

- [Use of double pointer in linux kernel Hash list implementation](https://stackoverflow.com/questions/3058592/use-of-double-pointer-in-linux-kernel-hash-list-implementation)
