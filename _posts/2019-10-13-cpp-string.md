---
layout: post
title: String in cpp
categories: [blog, cpp]
tags: [cpp]
---

* TOC
{:toc}

### Introduction

Strings are very common in every languages. The performance of string\'s methods usually
have a big impact on the whole program\'s speed. In this blog, we will investigate common
methods of a string.

### Convert to and from numbers

#### Convert a number into a string

There are two ways:
+ `to_string`
+ `ostringstream`

```cpp
int a = 3;
cout << std::to_string(a) << endl;

ostringstream os;
os << a;
cout << os.str() << endl;
```

#### Convert a number from a string

There are two ways:

+ `stoll`, `stol`, `stoi`, `stof, stod, stold`, `stoul`, `stoull`
+ `istringstream`

```cpp
string a = "3";
int b = stoi(a);

istringstream is(a);
a >> b;
```

### Construct a string

String is one of the sequence container like STL\'s `vector`.

+ default construct
+ repeat characters
+ from a c-style string
+ from a sequence
+ from a substring of another string

```cpp
#include <string>
using namespace std;
string a;
string b(3, 'c');
string c("hello world")
string d(c.begin(), c.end());
string e(c, 3, 4); // start from the third with a count equals 4
string f("hello", 3); // start from the first with a count equals 3
```

### Manipulate a string

#### Convert case

```cpp
#include <string>
#include <algorithm>
string a = "hEllO"
transform(a.begin(), a.end(), a.begin(), std::tolower);
transform(a.begin(), a.end(), a.begin(), std::toupper);
```

#### Add or remove element

+ `push_back`, `pop_back`
+ `append()`: similar to construct a string
  + append a range, a substring, repeating characters, etc.
+ `erase`
  + `erase(start_index, count)`
  + `erase(iterator)`
  + `erase(begin_iterator, end_iterator)`
+ `insert`
+ `substr(pos, count)`
+ `copy(dest, pos, count)`

#### Search, compare, replace

+ substring search
  + `find`
  + `rfind`
+ any character search
  + `find_first_of`
  + `find_first_not_of`
  + `find_last_of`
  + `find_last_not_of`
+ `compare`
  + -1, 0, 1
+ `replace`
  + `replace(pos, count1, count2, character)`
  + `replace(iter1, iter2, iter11, iter22)`

#### Hash values

C++ has provide a default implementation for `string` and many other types.

+ `bool`, integers, float and double, char
+ Pointer: please be aware that, c-style string hash is calculated as a pointer, not
using its content.

```cpp
#include <functional>
string a = "hello";
std::hash<string>()(a);

// customization of a hash

namespace std {
    template <>
    struct hash<Type> {
        size_t operator()(const Type& v) {
            return 0; // return v's hash value
        }
    };
}
```
