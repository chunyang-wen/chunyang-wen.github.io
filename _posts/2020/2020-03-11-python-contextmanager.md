---
layout: post
title: Python contextlib
categories: [blog, python]
tags: [python]
---

There are some resources we need to release when we finish our job. It is easy for us to forget
those operations. Python has a keyword *with* which can be used to help solve this problem.
After we go out the scope of with, python will make sure certain operations will be executed.

+ TOC
{:toc}

### Introduction

Python's module `contextlib` provides some common utilities to help write code which needs to
execute operations when leaving the scope.

### contextlib.contextmanager

This decorator makes any function which uses the `yield` keyword work with `with` clause.

```python
from contextlib import contextmanager


@contextmanager
def say_hi():
    print("HI")
    a = 3
    yield a
    print("Hello")


with say_hi() as a:
    print(a)
```

The statements before `yield` will be executed before entering `with`, the statements after
will be executed when leaving out the scope.

### contextlib.closing

Works with object which imlements a `close()` function such as a socket connection.

```python
from contextlib import closing


class Close(object):

    def say_hi(self):
        print("say hi")

    def close(self):
        print("closing")


with closing(CLose()) as close:
    close.say_hi()
```

### contextlib.ContextDecorator

It makes the instance as a contextmanager.

```python
from contextlib import ContextDecorator


class Manager(ContextDecorator):

    def __enter__(self):
        print("Entering")

    def __exit__(self, *exc):
        print("Exiting")


@Manager()
def fun():
    pass
```

### contextlib.suppress(\*excpetions)

Used to suppress exception. It is useful and can be used to replace the try/catch clauses.

```python
from contextlib import suppress, nullcontext

def fun():
    raise Exception("xx")

with suppress(Exception):
    func()

with nullcontext():
    func()
```

### contextlib.redirect_stdout/redirect_stderr

Redirect to other file handlers.

```python
from contextlib import redirect_stdout

def fun():
    print("HI")

with open("log", "w") as fd:
    with redirect_stdout(fd):
        func()
```
