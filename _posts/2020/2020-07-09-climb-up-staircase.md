---
layout: post
title: Climb up staircase
categories: [blog, algorithm]
tags: [dailycodingproblem, amazon]
include_math: true
---

+ toc
{:toc}

### Problem

This problem was asked by Amazon.

There exists a staircase with N steps, and you can climb up either 1 or 2 steps at a time.
Given N, write a function that returns the number of unique ways you can climb the staircase.
The order of the steps matters.

For example, if N is 4, then there are 5 unique ways:

1, 1, 1, 1
2, 1, 1
1, 2, 1
1, 1, 2
2, 2
What if, instead of being able to climb 1 or 2 steps at a time, you could climb any number
from a set of positive integers X? For example, if X = {1, 3, 5}, you could climb 1, 3, or 5
steps at a time.

### Solution

$$
F(n) = \sum{F(n-i)} \forall i
$$

```cpp
#include <iostream>
#include <vector>

int ways(const std::vector<int>& steps, int target) {
    std::vector<int> positions(target + 1, 0);
    positions[0] = 1;
    for (int i = 1; i <= target; ++i) {
        for (auto step : steps) {
            if (i - step >= 0) {
                positions[i] += positions[i-step];
            }
        }
        std::cout << "pos[" << i << "] = " << positions[i] << std::endl;
    }
    return positions[target];
}

int main() {

    std::cout << ways({1,2}, 4) << std::endl;

    return EXIT_SUCCESS;
}
```


### Reference

+ [Jump game](/blog/algorithm/jump-game.html)
