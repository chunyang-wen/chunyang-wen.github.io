---
layout: post
title: Run-length encoding
categories: [blog, algorithm]
tags: [dailycodingproblem, amazon]
hidden: true
---

+ toc
{:toc}

### Problem

This problem was asked by Amazon.

Run-length encoding is a fast and simple method of encoding strings.
The basic idea is to represent repeated successive characters as a single count and character.
For example, the string "AAAABBBCCDAA" would be encoded as "4A3B2C1D2A".

Implement run-length encoding and decoding. You can assume the string to be encoded have no
digits and consists solely of alphabetic characters.
You can assume the string to be decoded is valid.

### Solution

```cpp
#include <iostream>
#include <sstream>
#include <string>

using namespace std;

string encode(const string& str) {
    int prev = -1;
    int count = 0;
    ostringstream os;
    for (const char c: str) {
        if (prev == -1) {
            prev = c;
            count = 1;
        } else if (prev == c) {
            ++count;
        } else {
            os << count << (char)prev;
            prev = c;
            count = 1;
        }
    }
    if (count != 0)
        os << count << (char)prev;
    return os.str();
}

void test() {
    cout << encode("AABBCDEF") << endl;
    cout << encode("ABBBBCCDDDEEEF") << endl;
}

int main() {
    test();
    return 0;
}
```


