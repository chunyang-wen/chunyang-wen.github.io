---
layout: post
title: Containing water
categories: [blog, algorithm]
tags: [dailycodingproblem, facebook]
hidden: true
---

+ toc
{:toc}

### Problem

This problem was asked by Facebook.

You are given an array of non-negative integers that represents a two-dimensional elevation
map where each element is unit-width wall and the integer is the height. Suppose it will
rain and all spots between two walls get filled up.

Compute how many units of water remain trapped on the map in `O(N)` time and `O(1)` space.

For example, given the input `[2, 1, 2]`, we can hold `1` unit of water in the middle.

Given the input `[3, 0, 1, 3, 0, 5]`, we can hold `3` units in the first index,
`2` in the second, and `3` in the fourth index (we cannot hold `5` since it would run off
to the left), so we can trap 8 units of water.

### Solution

+ Find a maximum position and iterate from beginning and end to the position

```cpp
#include <iostream>
#include <vector>

using namespace std;


int containing_water(const vector<int>& walls) {
    int size = walls.size();
    int max_index = -1;
    int max_num = INT_MIN;
    for (int i = 0; i < size; ++i) {
        if (walls[i] >= max_num) {
            max_num = walls[i];
            max_index = i;
        }
    }

    int cur_max = 0;
    int water = 0;
    for (int i = 0; i < max_index; ++i) {
        water += max(cur_max - walls[i], 0);
        cur_max = max(cur_max, walls[i]);
    }
    cur_max = 0;
    for (int i = size - 1; i > max_index; --i) {
        water += max(cur_max - walls[i], 0);
        cur_max = max(cur_max, walls[i]);
    }
    return water;
}


void test() {
    cout << containing_water({2, 1, 2}) << endl;
    cout << containing_water({3, 0, 1, 3, 0, 5}) << endl;
}


int main() {
    test();
    return 0;
}

```


