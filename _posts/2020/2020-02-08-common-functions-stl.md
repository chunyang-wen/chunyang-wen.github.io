---
layout: post
title: Common functions implemented using STL
categories: [blog, cpp]
tags: [cpp]
---

+ toc
{:toc}

### Introduction

STL provides a lot of useful utilities. They can be used to implement interesting functions.

* This is a collection of this *

### Count lines

```cpp
int count_lines(string& file) {
    auto fd = ifstream(file.c_str();
    return count_if(
         istreambuf_iterator<char>(fd),
         istreambuf_iterator<char>(),
         [](c)->bool {return c == '\n';}
         ):
}
```

Please note that: `istream_iterator` won't work here. [Stackoverflow](https://stackoverflow.com/questions/10564013/c-streams-confusion-istreambuf-iterator-vs-istream-iterator)

Normally when you care:
+ formatted output, e.g. int/double, then use `istream_iterator`
+ unformatted input, raw bytes, use `istreambuf_iterator`

The same applies to `ostream_iterator` and `ostreambuf_iterator`.

### String trim

```cpp
void trim_left(string& input, function<bool(char)> fn) {
    input.erase(
        input.begin(),
        find_if(input.begin(), input.end(), [&](char c) {return !fn(c);})
    );
}

void trim_right(string& input, function<bool(char)> fn) {
    input.erase(
        find_if(input.rbegin(), input.rend(), [&](char c) {return !fn(c);}).base(),
        input.end()
    );
}
```

The `base()` function call is used to get the underlying iterator.

```cpp
string a = "";
std::reverse_iterator<std::string::iterator> ite = a.rbegin();
```

### Convert case

```cpp
string to_upper(string input) {
    transform(input.begin(), input.end(), ::toupper);
    return input;
}

string to_lower(string input) {
    transform(input.begin(), input.end(), ::tolower);
    return input;
}
```

### Split and Join strings


### Filter

```
template<typename Iterator, typename Pred>
void filter(Iterator beg, Iterator end, Iterator out, Pred p) {
    copy_if(beg, end, out, p);
}
```

### Map

```cpp
template<typename Iterator, typename Proc>
void map(Iterator beg, Iterator end, Iterator out, Proc p) {
    transform(beg, end, out, p);
}
```

### Reduce

```cpp
template<typename Iterator, typename Reduce, typename T>
T reduce(Iterator beg, Iterator end, T initial, Reduce r) {
    return accumulate(beg, end, initial, r);
}

```
