---
layout: post
title: Universal tree
categories: [blog, algorithm]
tags: [dailycodingproblem, google]
hidden: true
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

A unival tree (which stands for "universal value") is a tree where all nodes under it have the same value.

Given the root to a binary tree, count the number of unival subtrees.

For example, the following tree has 5 unival subtrees:

```cpp
    0

   / \

  1   0

     / \

    1   0

   / \

  1   1
```

### Solution

+ Assume an empty tree has no subtrees
+ All leaf nodes are unival subtrees
+ If a node is not a unival subtrees, then all its parents, parents of parents are not.

```cpp

struct TreeNode {
    int va;
    TreeNode* left;
    TreeNode* right;
};

int count_unival_substrees(TreeNode* root) {

    int count = 0;
    function<bool(TreeNode*)> traverse = [&](TreeNode* node) {
        if (!node) return true;
        if (!node->left && !node->right) {
            // early stop here
            ++count;
            return true;
        }
        bool left = traverse(node->left);
        bool right = traverse(node->right);
        if (!left || !right) return false;
        if (node->left && node->left-val != node->val) {
            return false;
        }
        if (node->right && node->right-val != node->val) {
            return false;
        }
        ++count;
        return true;
    };
    traverse(node);
    return count;
}
```
