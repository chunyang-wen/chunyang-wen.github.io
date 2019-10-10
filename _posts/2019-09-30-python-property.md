---
layout: post
title: Python descriptor
categories: [blog, python]
tags: [python]
---

Recently in my project, I need to **dynamically add property to an instance**. It is easy that any
class can support it.

```python

class AwesomeClass:
    def __init__(self):
        """
        Args:
            self
        """
        pass

# directly call `setattr` or `getattr`

c = AwesomeClass()

setattr(c, "hi", "hello")

setattr(c, "earth", "world")

c.hi = "3"

c.earth = 4
```

### Property

If we know all the property beforehand, we can define them in the class definition.

```python
class AwesomeClass:

    def __init__(self):
        #Args:

            #self

        self._hi = None

    @property
    def hi(self):
        return self._hi

    @property.setter
    def hi(self, new_hi):
        self._hi = new_hi
```

Or we can define it using the function property.

```python
class AwesomeClass:

    def __init__(self):
        self._hi = None

    def get_hi(self):
        return self._hi

    def set_hi(self, new_hi):
        self._hi = new_hi

    hi = property(fget=get_hi, fset=set_hi)

# full function signature

# property(fget=xxx, fset=xx, fdel=xx, doc=xx)

```

If we have defined them using `property`, how can can we get the property instance instead of the
real value?

```python
c = AwesomeClass()
prop = vars(type(c))["hi"]  # the property

# prop.setter(val)

# prop()

# prop.fset(val)

# prop.fget()
```

### Descriptor

`property` is actually an kind of descriptor. A descriptor is anything that defines:

+ `__get__(self, instance, owner)`: `owner` is `instance`'s type.
+ `__set__(self, instance, value)`
+ `__delete__(self, instance)`

```python
class Property(object):

    def __init__(self, val):
        self._val = val

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._val

    def __set__(self, instance, value):
        self._val = value

class AwesomeClass(object):
    pass

a = AwesomeClass()
setattr(a, "prop", Property(3))
```

Descriptor can be very interesting. For example, a cached property. A property is only
calculated when needed and following queries will reuse that value.

```python
import time

class CacheProperty(object):
    def __init__(self, fn):
        self._fn = fun

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self._fn(instance)
        vars(instance)[self._fn.__name__] = value
        return value


class A(object):

    @CacheProperty
    def b(self):
        time.sleep(1)
        return 3


a = A()
print(a.b)
print(a.b)

```
