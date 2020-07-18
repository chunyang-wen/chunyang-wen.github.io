---
layout: post
title: Enum in Cpp and Python
categories: [blog, common]
tags: [cpp, python]
---

`Enum` is very commonly used both in cpp and python. In this blog, we will introduce enumeration
in cpp and python.

+ toc
{:toc}

### Cpp

#### Unscoped enumeration

Old style of enumeration declaration does not have the concept of scope which means it is
globally accessed.

```cpp
#include <iostream>
using namespace std;

enum FileType {
    File = 0,
    Directory = 1,
    Link = 2,
    FileTypeCount,
};

enum Access {
    Read = 1,
    Write = 2,
    Exec = 4,
};

int main() {
    cout << FileTypeCount << endl;
    cout << Read << " " << (Read == 1) << endl;
    return 0;
}
```

#### Scoped enumeration

We add additional keyword `class` or `struct` after `enum`.

```cpp
#include <iostream>
using namespace std;

enum FileType {
    File = 0,
    Directory = 1,
    Link = 2,
    FileTypeCount,
};

enum Access {
    Read = 1,
    Write = 2,
    Exec = 4,
};

enum class NewAccess {
    Read = 8,
    Write = 16,
    Exec = 32,
};

ostream& operator<<(ostream& os, NewAccess na) {
    switch (na) {
        case NewAccess::Read: cout << "Read" << endl; break;
        case NewAccess::Write: cout << "Write" << endl; break;
        case NewAccess::Exec: cout << "Exec" << endl; break;
    }
    return os;
}


int main() {
    cout << FileTypeCount << endl;
    cout << Read << " " << (Read == 1) << endl;
    cout << NewAccess::Read << endl;
    // No unexplicit conversion here
    cout << (static_cast<int>(NewAccess::Read) == 8) << endl;
    return 0;
}

```

### Python

Normally in python, I will use the class variable as an enumeration.

```python
class Access:
    Read = 1
    Write = 2
    Exec = 4
```

But if we want get the name of the enumeration, we have to add them ourselves.

```python
from collections import namedtuple
class Item(namedtuple("Item", "name value")):
    pass

class Access:
    Read = Item("Read", 1)
    Write = Item("Write", 2)
    Exec = Item("Exec", 4)
```

In Python 3, we have a new module named `enum`.

```python
from enum import Enum

class Access(Enum):
    Read = 1
    Write = 2
    Exec = 4

print(Access.Read.name)
print(Access.Read.value)

Permission = Enum("Permission", "Allow Decline")
```

There are `unique` and `auto` in `enum.`

+ `unique`: a decorator to make sure not conflict values
+ `auto`: automatically generate values for each enumeration

An `enum` is iterable and each enumeration item can be used as the key of a dict. By default
an `enum` is not comparable besides `is` and `is not`. A subclass `IntEnum` supprt

### Reference

+ [CppReference](https://en.cppreference.com/w/cpp/language/enum)
+ [Python Doc](https://docs.python.org/zh-cn/3.7/library/enum.html)
