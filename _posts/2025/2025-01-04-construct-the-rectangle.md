---
layout: post
title: Construct the Rectangle
categories: [blog, leetcode]
tags: [leetcode]
---

This problem is a typical use case of double pointer in an array. Like in a sorted array, find
two elements who sum to a target number. This problem asks for the multiplication.

+ toc
{:toc}

Actually I was thinking a complicate method: find all the factors and try to come up with a
combination of the factors.

I couldn't find a correct way to find the solution. So I just try from 1 to the `area` and change
both either end when the product satisfies conditions

- `product > area`: move right end to left
- `product == area`: record the result and move both ends
- `product < area`: move left end to right

```cpp
class Solution {
public:
    vector<int> constructRectangle(int area) {
        int left = 1, right = area;
        vector<int> result{0, 0};
        while (left <= right) {
            long x = (long) left * right;
            if (x == area) {
                result[1] = left;
                result[0] = right;
                ++left;
                --right;
            } else if (x < area) {
                ++left;
            } else {
                --right;
            }
        }
        return result;
    }
};
```

It costs more than 100ms. It is not a good sign. I realize I can optimize it if we know either
end. For example, if we know `left`, we can get the other as `area/left`.

```cpp
class Solution {
public:
    vector<int> constructRectangle(int area) {
        int left = 1, right = area;
        vector<int> result{0, 0};
        while (left <= right) {
            long x = (long) left * right;
            if (x == area) {
                result[1] = left;
                result[0] = right;
                ++left;
                right = area / left;
            } else if (x < area) {
                ++left;
                right = area / left;
            } else {
                --right;
                left = area / right;
            }
        }
        return result;
    }
};
```

It is an easy problem but I think it takes me time to think and optimize it.
