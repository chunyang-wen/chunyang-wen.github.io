---
layout: post
title: How to exit nested loops
categories: [blog, cpp]
tags: [cpp]
hidden: true
---

+ TOC
{:toc}

### Introduction

Recently when solving [999\. Available Captures for Rook](https://leetcode.com/problems/available-captures-for-rook/),
I need to exit nested for loops. In C++, there seems not a better way to do it.

After searching google for a while, I found [this](https://stackoverflow.com/questions/1257744/can-i-use-break-to-exit-multiple-nested-for-loops).

### Use a `bool` flag

You have to check the specific flag at the end of each `for` loop.

```cpp
for (int i = 1; i < 3; ++i) {
    for (int j = 1; j < 3; ++j) {
        if (i+j == 2) {
            exited = true;break;
        }
    }
    if (exited) break;
}
```

### Use `goto`

```cpp
for (int i = 1; i < 3; ++i) {
    for (int j = 1; j < 3; ++j) {
        if (i+j == 2) goto EXIT;
    }
}
EXIT: int bingo = 1;
```

Usually `goto` means bad things, so use it at your own risk.

### Use lambda function

This is very interesting. I have been using a lot of `lambda`s in the code when sovling
leetcode problems. It will make the code short:

+ no need to define another function outside current function
+ no need to pass arguments around as you can capture them in the closure

**Use & to capture the value**

```cpp
// We assume you need the value of `i` and `j`.
int i, j;
[&](){
    for (i = 0; i < 3; ++i) {
        for (j = 0; j < 3; ++j) {
            if (i + j == 2) return;
        }
    }
}(); // remember to call the lambda function.
```
