---
layout: post
title: Minimum cost to color houses
categories: [blog, algorithm]
tags: [dailycodingproblem, facebook]
---

+ toc
{:toc}

### Problem

This problem was asked by Facebook.

A builder is looking to build a row of `N` houses that can be of `K` different colors. He has a
goal of minimizing cost while ensuring that no two neighboring houses are of the same color.

Given an `N` by `K` matrix where the `nth` row and `kth` column represents the cost to build
the `nth` house with `kth` color, return the minimum cost which achieves this goal.

### Solution

+ Backtracking with memorization
+ `mem[n][prev_sel]`:
  + If previous selected color is `prev_sel`, minimum cost from `nth` house.

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <functional>

using namespace std;

int minimum_coloring_cost(const vector<vector<int>> & price) {
    int N = price.size();
    int K = price[0].size();
    vector<vector<int>> mem(N, vector<int>(K, -1));
    function<int(int, int)> traverse = [&](int n, int prev_sel) {
        if (n == N) {
            return 0;
        }
        if (mem[n][prev_sel] != -1) {
            cout << "Hit: " << mem[n][prev_sel] << endl;
            return mem[n][prev_sel];
        }

        int cur = INT_MAX;
        for (int i = 0; i < K; ++i) {
            if (i == prev_sel) continue;
            cur = min(cur, price[n][i] + traverse(n+1, i));
        }
        if (prev_sel != -1)
            mem[n][prev_sel] = cur;
        return cur;
    };

    return traverse(0, -1);
}

int main() {

    // assume 5 houses, 4 color
    vector<vector<int>> price{ {1,2,3,4}, {7,1,3,9}, {8,19,2,1}, {7,19,1,10}, {100,39,1,2} };
    cout << minimum_coloring_cost(price) << endl;

    return 0;
}
```
