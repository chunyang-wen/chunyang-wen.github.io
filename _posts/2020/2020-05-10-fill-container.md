---
layout: post
title: How to fill a container?
categories: [blog, stl]
tags: [cpp]
---

Most of the time we initialize an empty instance of STL containers and keep
adding elements to or removing elements from it. For example, we create a `vector` and `push_back`
elements. But what if we want to fill a couple of initial elements?

+ toc
{:toc}

### Sequence container

+ `vector`
+ `deque`
+ `string`

### Use initilizer list

Almost all the conatiner types support this kind of initilization.

```cpp
vector<int> a{1,2,3};
deque<int> b{4,5,6};
```

#### Fill the same number

```cpp
vector<int> a(10);
fill(begin(a), end(a), 0);

deque<int> b(10);
fill(begin(b), end(b), 0);
```

#### Fill custom numbers

```cpp
vector<int> a(10);
int i = 0;
auto x = [&]() {return i++;};
generate(begin(a), end(a), x);

deque<int> b(10);
generate(begin(b), end(b), x);

```

#### Fill without predefined size

```cpp
vector<int> a;
fill_n(back_inserter(a), 10, 1);

deque<int> b;
fill_n(back_inserter(b), 10, 1);

vector<int> c;
int i = 0;
auto x = [&]() {return i++;};
int n = 10;
generate_n(back_inserter(c), n, x);

deque<int> d;
generate_n(back_inserter(d), n, x);
```

### Associative container

+ `set`, `unordered_set`
+ `map`, `unordered_map`

#### Initializer list

```cpp
set<int> a{1,2,3};
map<int, int> b{ {1,2}, {2,3} };
```

#### Fill different number

```cpp
set<int> a;
map<int, int> b;

int i = 0;
int n = 10;
generate_n(inserter(a, a.end()), n, [&]() {return i++;})
generate_n(inserter(b, b.end()), n, [&](){return make_pair(i++, 0);});
```

The iterators dereferenced from `set` or `map` is const which means we cannot directly modify it.

```cpp
set<int> a{3};
*a.begin() = 3;
```

Due to previous reasons, we cannot use `fill` or `fill_n` to fill `set` or `map`.

### Other possible methods

+ `swap`: swap two containers
+ `assign`: clean the elements and replace them
  + `vector`, `deque`, `string`
+ constructors

```cpp
vector<int> a{1,2,3};
vector<int> b;
b.swap(a);

vector<int> c;
c.assign(b.begin(), b.end());

vector<int> d(c);
vector<int> e(c.begin(), c.end());
```
