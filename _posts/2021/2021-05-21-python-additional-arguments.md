---
layout: post
title: Who passes the additional argument to my `fn` ?
categories: [blog, python]
tags: [python]
---

Recently in an implementation of a functionality, following error keeps showing and drives me crazy.


```python
Traceback (most recent call last):
  File "test_additional_parameter.py", line 13, in <module>
    fn(3)
TypeError: <lambda>() takes 1 positional argument but 2 were given
```

It is a really weird problem. It is a function which has only one parameter.

+ toc
{:toc}

### Minimal case

```python
from pprint import pprint


class Test:

    fn = lambda x: pprint(x)


a = Test()

fn = a.fn

fn(3)
```

It is obvious that you may guess `fn` is a function of an instance and it will receive
an argument `self` from the python interpreter.

> methods are functions, they are simply attached to the class,
> and when that function is called from an instance it gets that
> instance passed implicitly as the first argument automagically

After changing the method reference using a class, it works as expected.

```python
from pprint import pprint

class Test:
    fn = lambda x: pprint(x)

    @classmethod
    def fn1(cls, x):
        pprint(x)

a = Test.fn
a(3)

b = Test.fn1
b(4)
```

### Methods v.s. Functions, Arguments v.s. Parameters

We have already known the difference of a method and a function. There is also a similar
confusing pair: Parameters and Arguments. Parameters are the signature of a method or a
function while arguments are passed to the corresponding parameters' posistion.

### Reference

+ [Python method vs function Stackoverflow](https://stackoverflow.com/questions/46636190/python-method-vs-function)
+ [What's the difference between an argument and a parameter?](https://stackoverflow.com/questions/156767/whats-the-difference-between-an-argument-and-a-parameter#:~:text=A%20parameter%20is%20a%20variable,pass%20into%20the%20method's%20parameters.&text=Parameter%20is%20variable%20in%20the,that%20gets%20passed%20to%20function.)
