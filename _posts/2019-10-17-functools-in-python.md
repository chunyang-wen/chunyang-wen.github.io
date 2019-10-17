---
layout: post
title: functools in python
categories: [blog, python]
tags: [python]
---

* TOC
{:toc}

### Introduction

`functools` like `itertool` is very useful, but we pay little attention to it. It contains useful
tools in everyday life:

+ `wraps`
+ `cmp_to_key`
+ `partial`
+ `total_ordering`
+ `reduce`

### wraps

Python's decorator is very useful in many scenarios. But a decorator may break docstring,
signature of a function. `wraps` is used to fix this problem. By default, it will fix:
+ \_\_module\_\_
+ \_\_name\_\_
+ \_\_qualname\_\_
+ \_\_doc\_\_
+ \_\_annotations\_\_
+ \_\_dict\_\_: update this dict

Its implementation uses: `partial` and `functools.update_wrapper`. Usually we use it here:

```python
import functools

def decorator(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### cmp_to_key

`cmp_to_key` is used to solve the problem of API evovling. `sorted` method supports two
keyword arguments:
+ `cmp`
+ `key`

The suggested way is to use the `key` function. How to covert a compare function which
receives two arguments into a key function? `cmp_to_key` comes to help.

```python
from functools import cmp_to_key

a = [1,7,4,3]


def cmp(a, b):
    """Cmpare a and b"""
    return a < b

sorted(a, key=cmp_to_key(cmp))
```

### partial

Similar to C++'s `std::bind` function. It binds certain arguments of a function and return it.

```python
import functools as ft
from operator import add

a = 2
add_4 = ft.partial(add, 4)
print(add_4(2))
```

### total_ordering
This decorator dynamically generates all the order related methods. At least one of the
following methods is defined:

+ \_\_lt\_\_
+ \_\_le\_\_
+ \_\_gt\_\_
+ \_\_ge\_\_

And the other ordering methods will be generated using one of the above methods and the
sequence is the priority that `total_ordering` chooses to implement other methods.

```python
import functools

@functools.total_ordering
class Student(object):
    def __init__(self, height):
        self._height = height

    def __lt__(self, other):
        return self._height > other._height
```

### reduce

Similar to python's keyword: `reduce`

```python
import functools as ft
from operator import add

a = list(range(10))
print(ft.reduce(add, a))
print(ft.reduce(add, a, 10))

```
