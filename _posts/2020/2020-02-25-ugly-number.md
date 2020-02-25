---
layout: post
title: Ugly number I and II
categories: [blog, algorithm]
tags: [leetcode]
---

Ugly numbers are numbers which only divided by 2, 3, 5. By default 1 is also a ugly number.

+ toc
{:toc}

### Ugly Number I

Write a program to check whether a given number is an ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5.

Example 1:

> Input: 6
> Output: true
> Explanation: 6 = 2 × 3
> Example 2:

> Input: 8
> Output: true
> Explanation: 8 = 2 × 2 × 2
> Example 3:

> Input: 14
> Output: false
> Explanation: 14 is not ugly since it includes another prime factor 7.

*Note:*

+ 1 is typically treated as an ugly number.
+ Input is within the 32-bit signed integer range: [−231,  231 − 1].

Just implement it according to definitions.

```cpp
// 263. Ugly Number
// https://leetcode.com/problems/ugly-number/

class Solution {
public:
    bool isUgly(int num) {
        if (num <= 0) return false;
        while (num % 6 == 0) num /= 6;
        while (num % 10 == 0) num /= 10;
        while (num % 15 == 0) num /= 15;
        while (num % 2 == 0) num /= 2;
        while (num % 3 == 0) num /= 3;
        while (num % 5 == 0) num /= 5;
        return num == 1;
    }
};
```

### Ugly Number II

Write a program to find the n-th ugly number.

Ugly numbers are positive numbers whose prime factors only include 2, 3, 5.

Example:

> Input: n = 10
> Output: 12
> Explanation: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12 is the sequence of the first 10 ugly numbers.

*Note:*

+ 1 is typically treated as an ugly number.
+ n does not exceed 1690.

Directly test each number until we get enough number is one of the brute-force method.

We can expect a **TLE**.

```cpp
class Solution {
public:
    bool isUglyNumber(int num) {
        if (num <= 0) return false;
        while (num % 6 == 0) num /= 6;
        while (num % 10 == 0) num /= 10;
        while (num % 15 == 0) num /= 15;
        while (num % 2 == 0) num /= 2;
        while (num % 3 == 0) num /= 3;
        while (num % 5 == 0) num /= 5;
        return num == 1;

    }
    int nthUglyNumber(int n) {
        int cnt = 0;
        int i = 1;
        while (cnt < n) {
            if (isUglyNumber(i)) ++cnt;
            ++i;
        }
        return i-1;
    }
};
```

Each ugly number comes from a smaller ugly number multiplied by 2, 3, 5. So we can use three pointers
to point to previous smaller number so far.

```cpp
// 264. Ugly Number II
// https://leetcode.com/problems/ugly-number-ii/
class Solution {
public:
    int nthUglyNumber(int n) {
        vector<int> l(n);
        vector<int> p{0};
        l[0] = 1;
        for (int i = 1; i < n; ++i) {
            l[i] = min({l[p[0]] * 2, l[p[1]] * 3, l[p[2]] * 5});
            if (l[p[0]] * 2 == l[i]) ++p[0];
            if (l[p[1]] * 3 == l[i]) ++p[1];
            if (l[p[2]] * 5 == l[i]) ++p[2];
        }
        return l[n - 1];
    }
};
```

### Summary

It is a little like the prime test problem. To tell whether a number is a prime, we can directly
test it or use sieve algorithm. But actually they are used under different situations.

### Related

+ [Primality test](/blog/algorithm/primality-test)
