---
layout: post
title: Python closure
categories: [blog, python]
tags: [python]
---

Python closure usually makes code simpified and are used in functional programming style. It starts
with a keyword `lambda` and the last statement is the result returned. You can also create functions
inside another function. A `lambda` is a anonymous function.

+ toc
{:toc}

### Basic grammar

You can create a closure with the keyword `lambda`.

```python

import operator
from functools import reduce

a = [1, 2, 3]

# Increase each element in a and get a new list
b = list(map(lambda _: _ + 1, a))

# Get all even numbers
c = list(filter(lambda _: _%2==0, b))

d = reduce(operator.add, c, 0)
```

### Auto capture variables

A lambda function can automatically capture variables in its environment.

```python

def a():
    b = 3
    return lambda: b

c = a()
print(c())
```

But you need to be aware that there are boundaries where you can see a new variable.

+ Module: module level variables
+ Class: variables defined in a class
+ Function: variables defined in a function

If you are not familiar with those boundaries, you will make mistakes that you need to refer an
existing variable instead of creating a new variable.

```python
def func():
    a = 3
    def b():
        a = 4
    b()
    print(a)
```

The variable `a` is a new variable in function `b`, not the same variable in `a`.

#### Pitfall for capturing

```python
a = [1, 2, 3]

fns = []

for v in a:
    fns.append(lambda: v)
for fn in fns:
    print(fn())
```

We are expecting three different number printed on the screen. But actually 3 is repeated three
times. We are capturing the same variable. To fix the problem, we can add an argument to the
anonymous function and pass the argument. Python will evaluate the argument first.

#### You cannot use `print` in `lambda`

You cannot write `print` statement in a `lambda` function. But you can use `pprint` instead.

```python
from pprint import pprint

a = [1,2,3]

list(map(lambda _:pprint(_), a))

```

### References

+ [Common Gotchas](https://docs.python-guide.org/writing/gotchas/)
