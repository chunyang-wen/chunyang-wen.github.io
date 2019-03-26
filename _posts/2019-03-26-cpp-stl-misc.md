---
layout: post
title: C++ pair and type traits
categories: [cpp]
tags: [cpp, exception]
---

+ [简介](#intro)
+ [pair](#pair)
+ [type\_traits](#type-traits)

<a id="intro"></a>

### 简介

本文主要涵盖很多基础的点。

+ `pair`
+ `type_traits`

<a id="pair"</a>

### pair

定义一个 `struct`，有两个成员变量：

+ `first`
+ `second`

两个类型变量：

+ `first_type`
+ `second_type`

定义了两个基本的友元函数

+ `operator==`
+ `operator<`

其它都是通过这两个基本来实现的：`!=`, `>`，`>=`，`<=`

在实际使用中基本使用 `make_pair` 函数。

```cpp

#include <utility>

auto p = std::make_pair(3, 5);

```

<a id="type-traits"></a>

### type_traits

`type_traits` 主要是为模板编程辅助的，用于提取指定类型的特征，然后返回两种类型：

+ `__true_type`
+ `__false_type`

下面是一个完整的 traits 要指定的类型。这是一个模板类，模板的特化会为具体的类型指定对应的特征。

```cpp
template <class _Tp>
struct __type_traits {

   /* dummy for special purpose */
   typedef __true_type     this_dummy_member_must_be_first;


   typedef __false_type    has_trivial_default_constructor;
   typedef __false_type    has_trivial_copy_constructor;
   typedef __false_type    has_trivial_assignment_operator;
   typedef __false_type    has_trivial_destructor;
   typedef __false_type    is_POD_type;
};

/* 模板特化 */
struct __type_traits<bool> {
   typedef __true_type    has_trivial_default_constructor;
   typedef __true_type    has_trivial_copy_constructor;
   typedef __true_type    has_trivial_assignment_operator;
   typedef __true_type    has_trivial_destructor;
   typedef __true_type    is_POD_type;
};
```

对于常见的类型 `bool`, `char`, `unsigned char`, `wchar_t`, `signed char`, `short`, `unsigned short`,
`int`, `unsigned int`, `long`, `unsigned long`, `long long`, `unsigned long long`, `float`, `double`,
`long double` 都定义为 `__true_type`。

在注释中它举例如何使用这种技术。用户看到的是第一种 `copy` 的函数声明。但是实际上针对不同类型可能有
不同的高效实现，使用类型提取使得可以调用指定的实现版本，确不改变用户的接口，实现一种编译期的多态。

```cpp
void copy(T* source, T* target, int n);
void copy(T* source, T* target, int n, __true_type);
void copy(T* source, T* target, int n, __false_type);
```

本文完
