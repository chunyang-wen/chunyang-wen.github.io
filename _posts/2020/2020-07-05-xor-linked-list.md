---
layout: post
title: Xor linked list
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

An XOR linked list is a more memory efficient doubly linked list. Instead of each node
holding next and prev fields, it holds a field named both, which is an XOR of the next
node and the previous node. Implement an XOR linked list; it has an add(element) which adds
the element to the end, and a get(index) which returns the node at index.

If using a language that has no pointers (such as Python), you can assume you have access to
`get_pointer` and `dereference_pointer` functions that converts between nodes and memory addresses.

### Solution

+ Assume: `get(index)`, index >=0, a valid index

```cpp
#include <iostream>
using namespace std;

template<int n>
struct PointerSize {
    typedef int Type;
};

template<>
struct PointerSize<8> {
    typedef long Type;
};

template<>
struct PointerSize<4> {
    typedef int Type;
};

typedef PointerSize<sizeof(int*)>::Type  PointerType;

struct ListNode {
    int val;
    PointerType both;
    ListNode(int v): val(v), both(0) {};
};

class XorLinkedList {
public:

    XorLinkedList() {
        head = tail = nullptr;
    }

    // TODO: support adding at head
    void add(int val) {
        cout << "Adding value: " << val << endl;
        if (tail == nullptr) {
            head = tail = new ListNode(val);
        } else {
            ListNode* new_node = new ListNode(val);
            tail->both = tail->both ^ (PointerType)(new_node);
            new_node->both = (PointerType)tail;
            tail = new_node;
        }
        cout << "head: " << head->val << " tail: " << tail->val << endl;
    }
    void print() {
        ListNode* node = head;
        PointerType prev = 0;
        while (node) {
            cout << node->val << ", ";
            ListNode* next = (ListNode*)(node->both ^ prev);
            prev = (PointerType)node;
            node = next;
        }
        cout << endl;
    }
    ListNode* get(int index) {
        int count = 0;
        ListNode* node = head;
        ListNode* prev = 0;
        while (count < index) {
            ListNode* next = (ListNode*)(node->both ^ (PointerType)prev);
            prev = node;
            node = next;
            ++count;
        }
        return node;

    }

private:
    ListNode* head;
    ListNode* tail;
};

int main() {
    XorLinkedList l;
    l.add(3);
    l.add(4);
    l.add(5);
    l.print();
    cout << l.get(2)->val << endl;
}
```

### Comments

+ Given a node, how to find the previous and next node?
