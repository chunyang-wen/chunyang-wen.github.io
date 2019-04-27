---
layout: post
title: Linked list cycle
categories: [algorithm]
tags: [leetcode]
---

+ [题目](#problem)
+ [解法](#solution)
  + [思路](#way)
  + [代码](#code)

<a id="problem"></a>

### 题目

#### 题目一

Given a linked list, determine if it has a cycle in it.

To represent a cycle in the given linked list, we use an integer pos which represents the position
(0-indexed) in the linked list where tail connects to. If pos is -1, then there is no cycle in the
linked list.

#### 题目二

Given a linked list, return the node where the cycle begins. If there is no cycle, return null.

To represent a cycle in the given linked list, we use an integer pos which represents the position
(0-indexed) in the linked list where tail connects to. If pos is -1, then there is no cycle in the
linked list.

**Note: Do not modify the linked list.**


<a id="solution"></a>

### 解法

<a id="way"></a>

#### 思路

思路主要是快慢指针(不知道出处是否是 `Elements of programming`)。

+ 慢指针每次移动一步
+ 快指针每次移动两步

如果存在环，则当慢指针进入环后，假设此时快指针和慢指针之间的距离为 (d)，那么两个指针各自走动，每次
二者之间的距离就会减一，最后会相遇。称这个相遇的点为：碰撞点(collision point)。

在找到碰撞点后，怎么找到连接点(connection point)，连接点是第一次进入圆环的点。这个分析在上面说的书
中有，主要做法时：

+ collision point 往前走一步，得到 p
+ head 和 p 一直往前走，二者相遇的点即为 connection point

**分析过程**

假设 handle size = h, cycle size = c, 快慢指针经过 n 次移动后相遇，此时：

+ 慢指针移动：n = h + d
+ 快指针移动：2n + 1 = h + d + m * c

令 `h = qc + r`, 可以得到 `d = c - r -1`

`h+d = h + c - r -1 = qc + r + c - r -1 = (q+1) * c - 1`，从这点再移动 `h+1` 步得到

`(q+1) * c + h`，这个和头结点到 connection point 是一样的。

<a id="code"></a>

#### 代码

```cpp
class Solution {
public:
    ListNode *detectCycle(ListNode *head) {
        if (!head) return head;
        ListNode* slow = head;
        ListNode* fast = head->next;
        while (slow != fast) {
            slow = slow->next;
            if (!fast) return fast;
            fast = fast->next;
            if (!fast) return fast;
            fast = fast->next;
        }

        // return fast; // we get collision point

        // fast is collision point

        fast = fast->next;
        while (head != fast) {
            head = head->next;
            fast = fast->next;
        }
        return head;
    }
};
```

上述代码经过简单修改就可以得到是否存在环（不返回 fast，break 后判断 fast 是否是空指针）

本文完
