---
layout: post
title: Binary tree traversal
categories: [blog, algorithm]
tags: [leetcode]
redirect_from:
 - /algorithm/binary-tree-traversal
---

+ [介绍](#intro)
+ [Preorder](#preorder)
+ [Inorder](#inorder)
+ [Postorder](#postorder)
+ [State machine](#statemachine)


<a id="intro"></a>

### 介绍

二叉树在面试过程中会经常遇到，经典问题是三种遍历方式中的一种（一般考查后续遍历，最难）。也会考查提
供两种遍历方式，用户用程序恢复二叉树。问题一般有递归和非递归方式（一般考查非递归，难一点）。本文介
绍三种问题的非递归解法，并且提供可以运行的程序。

三种遍历方式是：

+ 先序遍历：根节点，左子节点，右子节点
+ 中序遍历：左子节点，根节点，右子节点（二叉搜索树中生成有序数组）
+ 后续遍历：左子节点，右子节点，根节点

<a id="preorder"></a>

### Preorder

#### 基本数的定义，构造和打印

构造二叉树时，假定使用 `?` 表示空节点，例如 `1 ? 2` 表示：

>    1
>     \
>      2

```cpp
#include <deque>

#include <iostream>

#include <stack> // for  traversal

#include <string>

#include <vector>

using namespace std;

struct TreeNode {
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v): val(v), left(NULL), right(NULL) {}
    static TreeNode* create_tree(string str);
    static string str(TreeNode* node);
    static void free_node(TreeNode* node);
};

TreeNode* TreeNode::create_tree(string str) {
    if (str.empty()) return NULL;
    int length = str.size();
    vector<TreeNode*> nodes;
    for(int i = 0; i < length; ++i) {
        int j = i;
        if (str[j] == ' ') continue;
        if (str[j] == '?') {
            nodes.push_back(NULL);
            continue;
        }
        while (j < length && str[j]>='0' && str[j] <= '9') ++j;
        cout << str.substr(i, j - i) << endl;
        nodes.push_back(new TreeNode(stoi(str.substr(i, j - i))));
        i = j;
    }
    length = nodes.size();
    for (int i = 0; i < length; ++i) {
        if (!nodes[i]) continue;
        cout << "connecting node: " << nodes[i]->val << endl;
        if (2 * i + 1 < length) nodes[i]->left = nodes[2 * i + 1];
        if (2 * i + 2 < length) nodes[i]->right = nodes[2 * i + 2];
    }
    cout << "nodes size: " << nodes.size() << endl;
    return nodes[0];
}

string TreeNode::str(TreeNode* node) {
    string s;
    if (!node) return s;
    deque<TreeNode*> cur;
    deque<TreeNode*> next;
    cur.push_back(node);
    int count = 1;
    while (!cur.empty()) {
        string cur_layer;
        int cur_count = 0;
        while (!cur.empty()) {
            TreeNode* node = cur.front(); cur.pop_front();
            ++cur_count;
            if (node == NULL) {
                cur_layer += "? ";
            }
            else {
                cout << "stringize node: " << node->val << endl;
                cur_layer += to_string(node->val);
                cur_layer += " ";
                if (node->left)
                    next.push_back(node->left);
                if (node->right)
                    next.push_back(node->right);
            }
        }
        int remain_q = count - cur_count;
        cout << "remain ?: " << remain_q << " cur layer: " << cur_layer << endl;
        while (remain_q-- > 0) s += "? ";
        count <<= 1;
        s += cur_layer;
        cur.swap(next);
    }
    int j = s.size();
    cout << "string s: " << s << endl;
    while (j > 0 && (s[j-1] == ' ' || s[j-1] == '?')) --j;
    return s.substr(0, j);
}


void TreeNode::free_node(TreeNode* node) {
    if (!node) return;
    if (node->left) free_node(node->left);
    if (node->right) free_node(node->right);
    delete node;
}

int main(int argc, char* argv[]) {

    string str = "1 ? 3 ? ? ? 5 ? ? ? ? ? ? 6 70";
    cout << "creating: " << str << endl;
    TreeNode* node = TreeNode::create_tree(str);
    cout << "string: " << TreeNode::str(node) << endl;
    TreeNode::free_node(node);

    return 0;
}
```

#### 先序遍历

```cpp
vector<int> preorder(TreeNode* node) {
    vector<int> result;
    stack<TreeNode*> st;
    st.push(node);
    while (!st.empty()) {
        TreeNode* top = st.top();
        result.push_back(top->val);
        if (top->right) st.push(top->right);
        if (top->left) st.push(top->left);
    }
    return result;
}
```

<a id="inorder"></a>

### Inorder

```cpp
vector<int> inorder(TreeNode* node) {
    vector<int> result;
    stack<TreeNode*> st;
    TreeNode* cur = node;
    while (!st.empty() || cur) {
        while (cur) {
            st.push(cur);
            cur = cur->left;
        }
        cur = st.top(); st.pop();
        result.push_back(cur->val);
        cur = cur->right;
    }

    return result;
}
```

<a id="postorder"></a>

### Postorder

后续遍历时，我们需要避免重复遍历同一个节点。

```cpp
vector<int> postorder(TreeNode* node) {
    vector<int> result;
    stack<TreeNode*> st;
    st.push(node);
    TreeNode* prev = NULL;
    while(!st.empty()) {
        TreeNode* top = st.top();
        if (prev != NULL && (prev == top->right || prev == top->left)) {
            result.push_back(top->val);
            st.pop();
            prev = top;
        } else if (top->left == NULL && top->right == NULL) {
            result.push_back(top->val);
            st.pop();
            prev = top;
        } else {
            if (top->right) st.push(top->right);
            if (top->left) st.push(top->left);
        }
    }



    return result;
}
```

<a id="statemachine"></a>

### State machine

在 `Elements of programming` 中，有另外一个非常巧妙的解法。利用状态机来完成转换。

### 重新建立依赖关系遍历

非递归一般需要使用栈来辅助。空间复杂度高。有一种方法重新建立关系，在遍历后恢复树来遍历。

+ [GeeksforGeeks](https://www.geeksforgeeks.org/inorder-tree-traversal-without-recursion-and-without-stack/)
+ [Wikipedia](https://en.wikipedia.org/wiki/Tree_traversal#Morris_in-order_traversal_using_threading)

本文完
