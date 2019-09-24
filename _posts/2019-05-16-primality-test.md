---
layout: post
title: Prime related
categories: [blog, algorithm]
tags: [prime]
---

+ [Introduction](#intro)
+ [Code](#code)
  + [Primaility test](#p-t)
  + [Sieve](#s)
+ [其它](#o)

<a id="intro"></a>

### Introduction

[参考页面](https://en.wikipedia.org/wiki/Primality_test)

一般来说在面试中我们遇到的是 2 类问题：

+ 判断一个数是否是素数
+ 统计小于某个数的素数个数

最经典的素数检查法是检查从 `2` -> `sqrt(n)` 所有数，如果有能被整除的数，则说明它不是素数，反之它是素数.
还有一种加速的方法：所有的数都可以表示为：`6k-1`, `6k + 0`, `6k+1`, `6k+2`, `6k+3`, `6k+4`。其中只有
`6k-1` 和 `6k+1` 可能是素数。我们只需检测这些数能否被输入 `n` 整除即可，其它的可以被 `2,3`

第二个使用筛选法。筛选法的核心思想是：如果一个数是素数，那么它的倍数一定不是素数。

<a id="code"></a>

### Code

<a id="p-t"></a>

#### Primaility test

```cpp

bool is_prime(int n) {
    if (n < 2) return false;
    if (n < 4) return true;
    if (n % 2 == 0) return false;
    int root = sqrt(n);
    for (int i = 3; i <= root; i += 2) {
        if (n % i == 0) return false;
    }
    return true;
}

bool is_prime_fast(int n) {
    if (n < 2) return false;
    if (n % 2 == 0) return false;
    if (n % 3 == 0) return false;
    int i = 5;
    int w = 2;
    while (i * i <= n) {
        if (n % i == 0) return false;
        i += w;
        w = 6 - w;
    }
    return true;
}

```

<a id="s"></a>

#### Sieve

其原理是：所有以较小数作为因子的数都在每一轮被剔除。

```cpp
int prime_less(int n) {
    if (n < 2) return 0;
    vector<bool> flag(n+1, false);
    flag[0] = true;
    flag[1] = true;
    for (int i = 2; i <= n; i++) {
        if (!flag[i]) {

            // i 的整数倍都从素数集合中剔除

            for (int j = i * 2; j <= n; j += i) {
                flag[j] = true;
            }
        }
    }
    return count_if(flag.begin(), flag.end(), [](bool v) { return !v;});
}
```

<a id="o"></a>

### 其它

其它还有一些不确定性的检测方法，启发式的。例如费马检测，米勒检测。可以参考文章开头的链接。

本文完。
