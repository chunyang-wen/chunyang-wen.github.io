---
layout: post
title: Edit distance
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

The edit distance between two strings refers to the minimum number of character
insertions, deletions, and substitutions required to change one string to the other.
For example, the edit distance between “kitten” and “sitting” is three:
substitute the “k” for “s”, substitute the “e” for “i”, and append a “g”.

Given two strings, compute the edit distance between them.

### Solution

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

int edit_distance(const string a, const string b) {
    if (a.empty()) return b.size();
    if (b.empty()) return a.size();
    int size_a = a.size();
    int size_b = b.size();
    vector<vector<int>> distance(size_a+1, vector<int>(size_b+1, 0));
    for (int i = 0; i <= size_a; ++i) {
        distance[i][0] = i;
    }
    for (int i = 0; i <= size_b; ++i) {
        distance[0][i] = i;
    }
    for (int i = 1; i <= size_a; ++i) {
        for (int j = 1; j <= size_b; ++j) {
            bool same = a[i-1] != b[j-1];
            distance[i][j] = min({distance[i-1][j-1] + same, distance[i-1][j] + 1, distance[i][j-1]+1});
        }
    }
    return distance[size_a][size_b];
}

void test(const string a, const string b) {
    cout << "Distance: " << a << " -- " << b << " = " << edit_distance(a, b) << endl;
}

int main() {
    test("abc", "abc");
    test("a", "abd");
    test("kitten", "sitting");
    return 0;
}
```

