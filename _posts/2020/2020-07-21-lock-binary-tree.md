---
layout: post
title: Lock or unlock a binary tree
categories: [blog, algorithm]
tags: [dailycodingproblem, google]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

Implement locking in a binary tree. A binary tree node can be locked or unlocked only if all of
its descendants or ancestors are not locked.

Design a binary tree node class with the following methods:

`is_locked`, which returns whether the node is locked
`lock`, which attempts to lock the node. If it cannot be locked, then it should return false.
Otherwise, it should lock it and return true.
`unlock`, which unlocks the node. If it cannot be unlocked, then it should return false.
Otherwise, it should unlock it and return true.
You may augment the node to add parent pointers or any other property you would like.
You may assume the class is used in a single-threaded program, so there is no need for
actual locks or mutexes. Each method should run in `O(h)`, where `h` is the height of the tree.

### Solution

```cpp
#include <iostream>
#include <vector>
#include <string>
#include <map>

using namespace std;


struct TreeNode {
    TreeNode* left;
    TreeNode* right;
    TreeNode* parent;
    int val;
    int lock_count;
    bool is_locked;
    TreeNode(int v):
        val(v), left(nullptr), right(nullptr), lock_count(0), is_locked(false), parent(nullptr)
    {}
};

bool is_locked(TreeNode* n);

// n can be locked many times
bool lock(TreeNode* n) {
    if (!n) return true;
    // 0: no lock on descendants of current node
    bool can_be_locked = n->lock_count < 1;
    can_be_locked = can_be_locked && !is_locked(n->parent);
    if (!can_be_locked) return false;
    n->is_locked = true;
    // n->lock_count = 0;
    while (n->parent) {
        n->parent->lock_count += 1;
        n = n->parent;
    }
    return true;
}

bool unlock(TreeNode* n) {
    if (!n) return true;
    // 0: no lock on descendants of current node
    bool can_be_unlocked = n->lock_count < 1;
    can_be_unlocked = can_be_unlocked && !is_locked(n->parent);
    if (!can_be_unlocked) return false;
    if (n->is_locked) {
        while (n->parent) {
            n->parent->lock_count -= 1;
            n = n->parent;
        }
    }
    n->is_locked = false;
    return true;
}

bool is_locked(TreeNode* n) {
    if (!n) return false;
    return n->is_locked || is_locked(n->parent);
}


/*
 * {"a", "ab0", "ac1", "bd0", "de1"}
 */
TreeNode* create_tree(const vector<string>& t) {
    map<char, TreeNode*> m;
    TreeNode* root = nullptr;
    for (const string& ss: t) {
        char c = ss[0];
        TreeNode* cur = nullptr;
        if (m.find(c) == m.end()) {
            cur = new TreeNode(c);
            m[c] = cur;
        } else {
            cur = m[c];
        }
        if (ss.size() == 1) {
            root = cur;
            continue;
        }
        const char p = ss[1];
        TreeNode* node = nullptr;
        if (m.find(p) == m.end()) {
            node = new TreeNode(p);
            m[p] = node;
        } else {
            node = m[p];
        }
        char d = ss[2];
        cout << "connect: " << c << " and " << p << " direction: " << d << endl;
        node->parent = cur;
        if (d == '0') cur->left = node;
        else cur->right = node;
    }
    return root;
}

void free_tree(TreeNode* n) {
    if (!n) return;
    free_tree(n->left);
    free_tree(n->right);
    delete n;
    n = nullptr;
}


int main() {
    TreeNode* root = create_tree({"a", "ab0", "ac1", "bd0", "de1"});
    free_tree(root);
    cout << "lock d = " << lock(root->left->left) << endl;
    cout << "lock d again = " << lock(root->left->left) << endl;
    cout << "lock b = " << lock(root->left) << endl;
    cout << "unlock c = " << lock(root->right) << endl;
    cout << "unlock d = " << unlock(root->left->left) << endl;

    return 0;
}
```
