---
layout: post
title: Cdr and car of a pair
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

I have subscribed to a [website](https://dailycodingproblem.com). Every day an email will be
sent to my email about the description of the problem.

+ toc
{:toc}

### Problem

This problem was asked by Jane Street.

`cons(a, b)` constructs a pair, and `car(pair)` and `cdr(pair)` returns the first and
last element of that pair.

For example

> car(cons(3, 4)) returns 3,
>
> cdr(cons(3, 4)) returns 4.

Given this implementation of cons:

```python

def cons(a, b):
    def pair(f):
        return f(a, b)
    return pair
```

Implement `car` and `cdr`.

### Solution

It seems that the problem definition is not correct. `cons` returns a function which receives
a function that can build a pair.

So a fixed version of `cons`

```python
def cons(a, b):
    return a, b
```

So `cdr` and `car`:

```python

def car(pair):
    """Get the first element"""
    if isinstance(pair[0], tuple):
        return car(pair[0])
    return pair[0]

def cdr(pair):
    """Get the last element"""
    if isinstance(pair[1], tuple):
        return car(pair[1])
    return pair[1]
```
