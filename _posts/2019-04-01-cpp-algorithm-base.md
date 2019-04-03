---
layout: post
title: C++ STL algo base
categories: [cpp]
tags: [algorithm]
---

+ [简介](#intro)
+ [算法合集](#algo-col)
  + [swap related](#swap-related)
  + [comparison related](#compare-related)
  + [copy and fill related](#copy-fill-related)

<a id="intro"></a>

### 简介

函数列表：

+ swap related
  + `iter_swap`
  + `swap`
+ comparison related:
  + `min`
  + `max`
  + `mismatch`
  + `equal`
  + `lexicographical_compare/_3way`
+ copy and fill related
  + `copy`
  + `copy_backward`
  + `copy_n`
  + `fill`
  + `fill_n`

<a id="algo-col"></a>

### 算法合集

<a id="swap-related"></a>

### swap related

#### iter_swap

交换两个迭代器，主要是依赖迭代器要实现赋值构造函数。

```cpp
template <class _ForwardIter1, class _ForwardIter2, class _Tp>
inline void __iter_swap(_ForwardIter1 __a, _ForwardIter2 __b, _Tp*) {
  _Tp __tmp = *__a;
  *__a = *__b;
  *__b = __tmp;
}

template <class _ForwardIter1, class _ForwardIter2>
inline void iter_swap(_ForwardIter1 __a, _ForwardIter2 __b) {
  __iter_swap(__a, __b, __VALUE_TYPE(__a));
}
```

其中 `__VALUE_TYPE` 是个宏，本质是调用 `type_traits` 来获取对应的 `::value_type`.

#### swap

交换两个数

```cpp
template <class _Tp>
inline void swap(_Tp& __a, _Tp& __b) {
  _Tp __tmp = __a;
  __a = __b;
  __b = __tmp;
}
```

这两个 **swap** 的区别就是交换的类型不一样，`iter_swap` 我们期望是交换类似指针的输入，交换的是指针
背后的值，而不是指针本身的值。

<a id="compare-related"></a>

### comparison related

#### min & max

比较两个值的大小，支持传入第三个参数作为比较函数。

#### mismatch


`mismatch(Iter first1, Iter last1, Iter first2)`，返回值是一个 `pair<Iter, Iter>(first1, first2)`。
其实现就分别递进两个迭代器，直到停止出现，或者不相等出现。期望的是 `first2` 指向的集合比 `first1`
指向的集合长

```cpp
template <class _InputIter1, class _InputIter2>
pair<_InputIter1, _InputIter2> mismatch(_InputIter1 __first1,
                                        _InputIter1 __last1,
                                        _InputIter2 __first2) {
  while (__first1 != __last1 && *__first1 == *__first2) {
    ++__first1;
    ++__first2;
  }
  return pair<_InputIter1, _InputIter2>(__first1, __first2);
}
```

支持第4个参数传入比较函数。

#### equal

比较两个序列是否相等，同样是期望序列 `__first2` 指向的序列比 `__first1` 指向的序列长。

```cpp
template <class _InputIter1, class _InputIter2>
inline bool equal(_InputIter1 __first1, _InputIter1 __last1,
                  _InputIter2 __first2) {
  for ( ; __first1 != __last1; ++__first1, ++__first2)
    if (*__first1 != *__first2)
      return false;
  return true;
}
```

支持第4个参数传入比较函数。

#### lexicographical_compare

使用 `<` 比较迭代器的值

`lexicographical_compare(Iter first1, Iter last1, Iter first2, Iter last2)`。支持再传入一个参数
作为比较函数。

#### lexicographical_compare_3way

这个带 `3way` 会额外跳过相等的元素。

+ 小于：返回 -1
+ 等于：返回 0
+ 大于：返回 1

<a id="copy-fill-related"></a>

### copy and fill related

复制的实现有 `trivial` 的实现，直接使用 `memcpy`。`non-trivial` 的实现考虑到了不动 `iterator`。对于
`ForwardIterator` 按部就班移动即可，对于 `RandomAccessIterator` 则会计算距离差，然后通过移动整数来
作为判断条件。

+ `copy(Iter first, Iter last, Iter result)`
+ `copy_n(Iter first, size_type cnt, Iter result)`
+ `fill(Iter first, Iter last, _Tp val)`
+ `fill_n(Iter first, size_type n, _Tp val)`

本文完
