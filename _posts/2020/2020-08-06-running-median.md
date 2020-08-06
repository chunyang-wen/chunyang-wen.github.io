---
layout: post
title:
categories: [blog, algorithm]
tags: [dailycodingproblem, microsoft]
---

+ toc
{:toc}

### Problem

This problem was asked by Microsoft.

Compute the running median of a sequence of numbers. That is, given a stream of numbers,
print out the median of the list so far on each new element.

Recall that the median of an even-numbered list is the average of the two middle numbers.

For example, given the sequence `[2, 1, 5, 7, 2, 0, 5]`, your algorithm should print out:

```cpp
2
1.5
2
3.5
2
2
2
```

### Solution

+ Use a maximum queue and a minimum queue

```cpp

#include <iostream>
#include <vector>
#include <queue>

using namespace std;
typedef priority_queue<int, vector<int>, less<int>> MaxPQ;
typedef priority_queue<int, vector<int>, greater<int>> MinPQ;

void fix_queue(MaxPQ& left, MinPQ& right) {
    if (right.empty()) {
        while (left.size() > right.size()) {
            right.push(left.top());
            left.pop();
        }
    } else {
        while (!left.empty() && left.top() > right.top()) {
            right.push(left.top());
            left.pop();
        }
    }
    while (left.size() > right.size()) {
        right.push(left.top());
        left.pop();
    }
    while (left.size() < right.size()) {
        left.push(right.top());
        right.pop();
    }
}

void running_median(const vector<int>& data) {

    MaxPQ left;
    MinPQ right;
    for (int datum: data) {
        left.push(datum);
        fix_queue(left, right);
        if (left.size() == right.size()) {
            cout << (left.top() + right.top()) / 2.0 << ", ";
        } else if (left.size() > right.size()) {
            cout << left.top() << ", ";
        } else {
            cout << right.top() << ", ";
        }
    }
    cout << endl;
}


int main() {
    running_median({2, 1, 5, 7, 2, 0, 5});
    return 0;
}
```


