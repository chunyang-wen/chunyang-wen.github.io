---
layout: post
title: K node from end
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

Given a singly linked list and an integer `k`, remove the `kth` last element from the list.
`k` is guaranteed to be smaller than the length of the list.

The list is very long, so making more than one pass is prohibitively expensive.

Do this in constant space and in one pass.

### Solution

+ Be careful when it is the head to be deleted.

+ [Utility.cpp](https://github.com/chunyang-wen/code-practice/tree/master/dailycodingproblem)

```cpp
#include <iostream>
#include <cassert>
#include "utility.hpp"

using namespace std;

/*
 * k = 2
 * 1 -> 2 -> 3 -> 4 -> 5
 */
ListNode* remove_k_node_from_end(ListNode* head, int k) {
    ListNode* fast = head;
    ListNode* slow = head;
    ListNode* prev = head;
    int steps = k - 1;
    while (steps-- > 0) fast = fast->next;
    cout << "fast->val = " << fast->val << endl;
    assert(fast != nullptr);
    while (fast->next != nullptr) {
        fast = fast->next;
        prev = slow;
        slow = slow->next;
    }
    prev->next = slow->next;
    if (slow == head) head = head->next;
    slow->next = nullptr;
    delete slow;
    return head;
}

int main(int argc, char* argv[]) {

    ListNode* node = make_list({1,2,3,4,5});
    int k = stol(argv[1]);
    node = remove_k_node_from_end(node, k);
    print_list(node);
    cout << endl;


    free_list(node);


    return 0;
}
```
