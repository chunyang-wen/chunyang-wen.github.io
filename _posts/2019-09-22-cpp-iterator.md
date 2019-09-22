---
layout: post
title: C++ Iterator
categories: [cpp]
tags: [cpp, exception]
---

+ [Introduction](#intro)
+ [Common Iterator Wrapper](#common-iterator-wrapper)
  + [Inserters](#inserter)
  + [IO related](#io-related)
+ [Common functions](#common-iterator-func)

<a id="intro"></a>

### Introduction

`Iterator` is an essential part in STL. We can use iterator to:
+ traverse the elements of sequence or associative containers.
+ work with STL's algorithm

There are five kinds of `iterators`:

+ Input Iterator
  + Forward Iterator: only moves ahead
  + Bidirectional Iterator: can move forward or backward
  + Random Access Iterator: can randomly any valid position
+ Output Iterator
  + All above three iterators can be an output iterator.

<a id="common-iterator"></a>

### Common Iterator Wrapper

<a id="inserter"></a>

#### Inserters

+ `front_inserter`
+ `back_inserter`
+ `inserter`

In most STL's algorithms, users are responsible for allocating space for the output. But most
time we donot know the space we need in advance. For example, `copy`

```cpp
vector<int> source{1,2,3};
vector<int> target;
copy(source.begin(), source.end(), target.begin());
```

The above program may crash. We can fix it by initializing the `target` with a size of
`source.size()`. It is easy that we forget this kind of initialization. `back_inserter` comes to
help here.

```cpp
copy(source.begin(), source.end(), back_inserter(target));
```

`back_inserter` turns the moving the forward operation into a `push_back` operation.

```cpp
vector<int> source{1,2,3};
deque<int> target;
set<int> s;

// the same with: `front_inserter` and `inserter`

copy(source.begin(), source.end(), front_inserter(target));
copy(source.begin(), source.end(), inserter(s, s.end()));
```

<a id="io-related-iterator"></a>

#### IO related

+ `istream_iterator`
  + used to consume input stream
+ `ostream_iterator`
  + used to print values

##### istream\_iterator

```cpp
vector<int> v;
istringstream s("1 2 3");

istream_iterator<int> ii(s);
copy(ii, istream_iterator<int>(), back_inserter(v));
```

It automatically coverts the input stream to the specified data type and put them
into the container.

##### ostream\_iterator

If we want to print all the elements in a container, how can we implement it? We can use a `range`
for clause.

```cpp
vector<int> v{1,2,3};
for (int vv: v) {
    cout << vv << ", "
}
cout << endl;

//^1, 2, 3, $
```

We can also use a `ostream_iterator`.

```cpp
copy(v.begin(), v.end(), ostream_iterator<int>(cout, ", "));
cout << endl;

//^1, 2, 3, $
```

<a id="common-iterator-func"></a>

### Common functions

+ `advance(iter, distance)`: no iterator returned
+ `distance(start_iter, end_iter)`: returns the distance
+ `next(iter, distance=1)`: returns updated iterator
+ `prev(iter, distance=1)`: returns updated iterator
+ `begin(container)`: returns the starting iterator
+ `end(container)`: returns the last iterator
