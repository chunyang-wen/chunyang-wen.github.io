---
layout: post
title: Bracket match
categories: [blog, algorithm]
tags: [dailycodingproblem, facebook]
---

+ toc
{:toc}

### Problem

This problem was asked by Facebook.

Given a string of round, curly, and square open and closing brackets,
return whether the brackets are balanced (well-formed).

For example, given the string `"([])[]({})"`, you should return true.

Given the string `"([)]"` or `"((()"`, you should return false.

### Solution

```cpp
#include <iostream>
#include <string>
#include <stack>
#include <map>

using namespace std;


bool bracket_match(const string& str) {
    stack<char> st;
    map<char, char> m { {')', '('}, {']', '['}, {'}', '{'} };
    for (char c: str) {
        switch (c) {
            case '(':
            case '[':
            case '{':
                st.push(c); break;
            case ')':
            case ']':
            case '}':
                if (st.empty() || st.top() != m[c]) return false;
                st.pop();
                break;
            default:
                break;
        }
    }
    return st.empty();
}

int main() {

    cout << bracket_match("([])[]({})") << endl;
    cout << bracket_match("([)]") << endl;
    cout << bracket_match("((()") << endl;
    return 0;
}
```
