---
layout: post
title: At most distinct K
categories: [blog, algorithm]
tags: [dailycodingproblem, amazon]
---

+ toc
{:toc}

### Problem

This problem was asked by Amazon.

Given an integer k and a string s, find the length of the longest substring that contains at
most k distinct characters.

For example, given s = "abcba" and k = 2, the longest substring with k distinct characters is
"bcb".

### Solution

We use a `map` to record current met characters and their count.

+ `i` represents the starting position
+ `j` represents the ending position

```cpp
#include <iostream>
#include <string>
#include <map>

using namespace std;

int longest_substring(const string& s, int k) {
    map<char, int> m;
    int i = 0, j = 0;
    int result = -1;
    int size = s.size();
    while (j < size) {
        if (m.size() == k) {
            if (m.find(s[j]) == m.end()) {
                while (m.size() >= k) {
                    m[s[i]]--;
                    if (m[s[i]] == 0) {
                        m.erase(s[i]);
                    }
                    ++i;
                }
            }
        }
        ++m[s[j]];
        ++j;
        result = max(result, j - i);
    }
    return result;
}

int main() {

    cout << longest_substring("abcba", 2) << endl;

    return EXIT_SUCCESS;
}
```
