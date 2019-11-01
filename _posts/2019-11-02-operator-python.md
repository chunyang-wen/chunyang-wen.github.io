---
layout: post
title: operator module in Python
categories: [blog, python]
tags: [python]
---

* TOC
{:toc}

### Introduction

Python's `operator` module provides us a lot of useful functions. We can write less **lambda**
functions.

### Common operator

+ `add/sub/mul/floordiv/truediv`
+ `mod`, `imod`
+ `pow`
+ `neg`, `pos`
+ `abs`

The `i*` is the corresponding part of swapping the arguments. For example if `a + b` fails due to
the missing definition of operator `+` for a, Python will try to swap them and call `b+a`.

### Relation

+ `ge/gt`
+ `le/lt`
+ `eq/ne`
+ `not_`
+ `is_not`
+ `is_`
+ `truth`

### Bit operations

+ `lshift`, `rshitf`
+ `xor`
+ `or_`
+ `and_`
+ `inv`, `invert`

### Elements and attributes

+ `attrgetter`
+ `itemgetter`
+ `setitem(a, b, c)`: *a[b] = c*
+ `delitem(a, b)`: *del a[b]*
+ `contains(a, b)`: `b in a`

### Other

+ `countOf(a, b)`
+ `indexOf(a, b)`
+ `concat(a, b)`: a + b as sequence
+ `methodcaller`: return a callable object
  + methodcaller(a)(r) equals: r.a()
  + methodcaller(a, c, b=3)(r) equals: r.a(c, b=3)

### Examples

```python
import operator as op
# reduce an array

a = [1, 2, 3]
reduce(op.add, a, 0)

b = [[0, 1], [2, 3], [3, 4]]
reduce(op.add, map(op.itemgetter(0), b), 0)

b = [{"0": 1}, {"0": 3}, {"0": 4}]
reduce(op.add, map(op.itemgetter("0"), b), 0)

class A: pass
c = A()
c.a = 3
d = A()
d.a = 4
list(map(op.attrgetter("a"), [c, d]))


b = [{"0": 1}, {"0": 3}, {"1": 4}]
[op.contains("0", bb) for bb in b]
list(map(lambda x:op.contains(b, x), b))

```
