---
layout: post
title: Decode ways
categories: [blog, algorithm]
tags: [dailycodingproblem, facebook]
---

+ toc
{:toc}

### Problem

This problem was asked by Facebook.

Given the mapping a = 1, b = 2, ... z = 26, and an encoded message, count the number of ways it can be decoded.

For example, the message '111' would give 3, since it could be decoded as 'aaa', 'ka', and 'ak'.

You can assume that the messages are decodable. For example, '001' is not allowed.

### Solution

We try string of length 1 or 2 for each position.

+ If it is valid, then continue
+ If not, stop

```cpp
int decode_ways(const string& input) {
    int count = 0;
    int size = input.size();
    function<void(int)> decode = [&](int start) {
        if (start == size) {
            ++count;
            return;
        }
        if (input[start] == '0') return;
        decode(start+1);
        if (start+1 >= size) return;
        int next = start+1;
        if (input[start] == '1' && input[next] >= '0' && input[next] <= '9') {
            decode(start+2);
        }
        if (input[start] == '2' && input[next] >= '0' && input[next] <= '6') {
            decode(start+2);
        }
    };
    decode(0);
    return count;
}
```

