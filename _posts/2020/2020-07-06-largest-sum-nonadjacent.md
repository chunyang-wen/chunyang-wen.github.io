---
layout: post
title: Maximum non-adjacent sum
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

This problem was asked by Airbnb.

Given a list of integers, write a function that returns the largest sum of non-adjacent
numbers. Numbers can be 0 or negative.

For example, [2, 4, 6, 2, 5] should return 13, since we pick 2, 6, and 5.
[5, 1, 1, 5] should return 10, since we pick 5 and 5.

Follow-up: Can you do this in O(N) time and constant space?

### Solution

Dynamic programming. For each position i: F(i) means the largest non-adjacent sum until position
i (inclusive). Assume the array is n:

F(0) = n[0]

F(1) = max(n[0], n[1])

F(i) = max(F(i-1), F(i-2) + (0 if n[i] <= 0 else n[i]))

```cpp
int max_nonadjacent_sum(vector<int>& n) {
    int size = n.size();
    if (size == 1) return n[0];
    if (size == 2) return max(n[0], n[1]);
    int f0 = n[0];
    int f1 = max(n[0], n[1]);
    for (int i = 2; i < size; ++i) {
        auto cur = n[i] <= 0 ? 0: n[i];
        auto tmp = max(f1, f0 + cur);
        f0 = f1;
        f1 = tmp;
    }
    return f1;
}
```
