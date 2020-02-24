---
layout: post
title: abc module in Python
categories: [blog, python]
tags: [python]
---

* TOC
{:toc}

### Introduction

abc is short for Abstract Base Class. Usually we use it to create a base class and
force the subclass to implement certain functions. In python, `abc` is similar to
C++'s abstract class.

There are three ways we can create this kind of class.

```python
from abc import ABC, ABCMeta
from abc import abstractmethod

class Base1(ABC):
    @abstractmethod
    def hi(self):
         raise NotImplementedError("HH")

class Base2(metaclass=ABCMeta):
    @abstractmethod
    def hi(self):
        raise NotImplementedError("HH")

class Base3(object):
    __metaclass__ = ABCMeta
    @abstractmethod
    def hi(self):
        raise NotImplementedError("HH")
```


### `abc` Module

+ `ABCMeta`
  + This should be the meta class of any class that wants to be the abc.
+ `ABC`
  + Just a simple wrapper, its meta class = `ABCMeta`. Users can directly inherit from it.
+ `ABCMeta.register`
  + Dynamically register any class and `issubclass`, `isinstance` will return
`True` after registration.
  + Will not affect the MRO mechanism
+ `abstractmethod`:
  + If working with other decorators, please make sure that this is the first one. For example
  working with `property` or `classmethod`

### `collections.abc` Module

<a href="https://docs.python.org/3/library/collections.abc.html#module-collections.abc"
target="_blank"> Reference </a>


|        Class     |   Inherits from  | Required methods     | Mixin methods|
| :------------------ | :------------ | :-------------------------|:--------------------------|
|Sized||\_\_len\_\_||
|Awaitable||\_\_await\_\_||
|Coroutine|Awaitable|send;throw|close|
|AsyncIterable||\_\_aiter\_\_||
|AsyncIterator|AsyncIterable|\_\_anext\_\_|\_\_aiter\_\_|
|ASyncGenerator|AsyncIterator|asend, athrow|aclose|
|Iterable||\_\_iter\_\_||
|Callable||\_\_call\_\_||
|Hashable||\_\_hash\_\_||
|Reversable|Iterable|\_\_reversed\_\_||
|Iterator|Iterable|\_\_next\_\_|\_\_iter\_\_|
|Generator|Iterator|send, throw | close, \_\_iter\_\_, \_\_next\_\_|
|Container||\_\_contains\_\_|
|MutableSequence||
|Collection|Container<br/>Iterable<br/>Sized|\_\_contains\_\_<br/>\_\_iter\_\_<br/>\_\_len\_\_|
|Sequence|Reversable<br/> Collection|\_\_getitem\_\_;\_\_len\_\_|\_\_contains\_\_;\_\_iter\_\_<br/>\_\_reversed\_\_;index;count|
|MutableSequence|Sequence|\_\_getitem\_\_;\_\_setitem\_\_<br/>\_\_delitem\_\_;\_\_len\_\_;insert|Inherited from Sequence,append<br/>reverse,extend, pop, remove, \_\_iadd\_\_|
|ByteString|Sequence|\_\_getitem\_\_, \_\_len\_\_|Inherit from Sequence|
|Set|Collection|\_\_contains\_\_ <br/> \_\_iter\_\_,\_\_len\_\_|\_\_le\_\_, \_\_lt\_\_, \_\_eq\_\_, \_\_ne\_\_, \_\_gt\_\_, \_\_ge\_\_<br/> \_\_and\_\_, \_\_or\_\_, \_\_xor\_\_, \_\_sub\_\_, isdisjoint|
|MutableSet|Set|\_\_contains\_\_ <br/> \_\_iter\_\_, \_\_len\_\_, add, discard|Inhert from Set, clear, pop <br/> remove<br/> \_\_ior\_\_, \_\_iand\_\_, \_\_ixor\_\_, \_\_isub\_\_|
|Mapping|Collection|\_\_getitem\_\_, \_\_iter\_\_, \_\_len\_\_|\_\_contains\_\_, keys, items, values <br/> get, \_\_eq\_\_, \_\_ne\_\_|
|MutableMapping|Mapping|\_\_getitem\_\_, \_\_setitem\_\_ <br/>\_\_delitem\_\_<br/>\_\_iter\_\_, \_\_len\_\_|pop, popitem <br/> clear, update, setdefault|

`*View` related base classes are ommited.

### Animal example

```python
from abc import ABC, abstractmethod

class Animal(ABC):

    @abstractmethod
    def talk(self):
        pass

class Dog(Animal):

    def talk(self):
        print("Wang!")

class Cat(Animal):

    def talk(self):
        print("Meow!")


class Snake(object):

    def x(self):
        print("x")

Animal.register(Snake)

class Bird(Animal):
    pass

Dog().talk()
Cat().talk()
print(issubclass(Snake, Animal)) # True
print(isinstance(Snake(), Animal)) # True
# TypeError: Can't instantiate abstract class Bird with abstract methods talk
bird = Bird()
```

### AwesomeSequence

```python
from collections.abc import Iterable

class AwesomeSequence(Iterable, Callable):

    def __init__(self):
        self._a = 1
        self._b = 0
        self._c = 2
        self._d = 4

    def __iter__(self):
        yield self._a
        yield self._b
        yield self._c
        yield self._d

    def __call__(self):
        return iter(self)

c = AwesomeSequence()
for v in iter(c):
    print(v)

for v in c():
    print(v)

```

### Recommended reading:

+ [Python magic methods](/blog/translating/a-guide-to-python-magic-methods.html)

[1]: https://docs.python.org/3/library/abc.html
[2]: https://docs.python.org/3/library/collections.abc.html#module-collections.abc
[3]: https://pymotw.com/2/abc/
