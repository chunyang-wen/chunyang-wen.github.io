---
layout: post
title: Descriptor and decorator in Python
categories: [blog, python]
tags: [python]
redirect_from:
 - /python/python-descriptor-decorator
---

装饰器 (Decorator) 模式是为既有的功能增加新的功能，例如都是标题，可以不改变原来的代码，增加一个加粗
的功能。

在 `Python` 中增加一个修饰器很简单，只要使用语法 `@decorator` 即可。

### 增加一个普通装饰器

```python
def say_hello(name):
    print '{name}hello'.format(name=name)
```

上述是一个简单的问候函数，现在需要根据 `name` 的级别，额外输出一些信息。

```python
def is_beggar_vip(name):
    vips = ['z', 'l']
    return name in vips

def say_vip(func):
    def inner(name):
        if is_beggar_vip(name):
            print '{name} warmly welcome'.format(name=name)
        return func(name)
    return inner

@say_vip
def say_hello(name):
    print '{name} hello'.format(name=name)

say_hello('l')
say_hello('w')
```

`say_vip` 这个修饰器的输入参数是其要装饰的函数，他要返回一个 `callable` 的对象，这个 `callable` 对象会被调用。如果我们需要修饰某个对象的函数，那么在返回的 `callable` 对象的接口需要增加 `self`。可以通过 `*args` 和 `**kwargs` 的方式来增加通用的修饰器

```python
def decorator(func):
    def inner(name, *args, **kwargs):
        # do some stuff
        return func(name, *args, **kwargs)
    return inner
```

如果对部分参数的有依赖，可以将其从 `*args` 或者 `**kwargs` 中单独拿出来，但是在调用 `func` 时要继续传入。

### 增加带参数的装饰器

根据参数对装饰器进行进行定制。这个函数不仅返回一个 `callable` 对象，而且这个 `callable` 是一个装饰器，这个装饰器要返回另外一个 `callable` 对象。

+ `say_vip`: 是带参数的装饰器
+ `company_A_decorator`, `normal_decorator`: 是类似于正常的装饰器
+ `inner`: 是装饰器返回的装饰过的函数

```python
def is_beggar_vip(name):
    vips = ['z', 'l']
    return name in vips

def is_company_A(name):
    company_A = ['l']
    return name in company_A

def say_vip(status):
    if status == 'sub-company-A':
        def company_A_decorator(func):
            def inner(name):
                print 'Welcome from company A'
                if is_beggar_vip(name) and is_company_A(name):
                    print '{name} warmly welcome'.format(name=name)
                return func(name)
            return inner
        return company_A_decorator
    else:
        def normal_decorator(func):
            def inner(name):
                print 'Welcome from company'
                if is_beggar_vip(name):
                    print '{name} warmly welcome'.format(name=name)
                return func(name)
            return inner
        return normal_decorator

@say_vip('sub-company-A')
def say_hello(name):
    print '{name} hello'.format(name=name)

say_hello('l')
say_hello('w')
```

### 描述符 (Descriptor)

描述符有三个函数需要实现(称作协议)：

+ `__set__`
+ `__get__`
+ `__delete__`

Descriptor 和 Decorator 的概念很接近。 Decorator 用于给函数增加属性。Descriptor 相对于 Decorator 更加的通用。其一般用于类的属性描述。 Descriptor 是作用于类的属性，所有用户需要自己维护不同实例的属性。

主要参考 [Reference][1]

```python
from weakref import WeakKeyDictionary
class Price(object):
    def __init__(self):
        self.values = WeakKeyDictionary()

    def __get__(self, instance, ownerclass=None):
        return self.values[instance]
    
    def __set__(self, instance, value):
        self.values[instance] = value
    
    def __delete__(self, instance):
        del self.values[instance]

class Book(object):
    price = Price()

b = Book()
b.price = 10
print b.price
```

在上述代码中，我们创建了一个 Descriptor, 其负责 `price` 的读和写。使用 `self.values` 来保存不同实例的值。如果不使用 `self.values` 来保存不同实例的值，会造成各个不同实例相同属性的互相覆盖。

`Python` 还提供了 
+ `@property` 的修饰器
+ `property(fget=None, fset=None, fdel=None, doc=None)`

```python
class Book(object):

    def __init__(self, name, price):
        self._price = price
        self._name = name

    @property
    def price(self):
        return self._price

    @price.setter:
    def price(self, price):
        self._price = price

    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name
    def delete_name(self):
        del self._name
    name = property(get_name, set_name, delete_name)
```

[1]: https://www.smallsurething.com/python-descriptors-made-simple/
