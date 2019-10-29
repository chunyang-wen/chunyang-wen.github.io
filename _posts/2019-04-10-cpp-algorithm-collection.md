---
layout: post
title: C++ STL algorithm
categories: [blog, stl]
tags: [cpp]
redirect_from:
 - /cpp/cpp-algorithm-collection
---

+ [简介](#intro)
+ [一些 notes](#notes)
+ [sort 相关](#sort)
+ [merge 相关](#merge)

<a id="intro"></a>

### 简介

本文主要介绍 `stl_algo.h` 中暴露的算法接口。

+ `__median`
+ `for_each(Iter first, Iter last, _Fun f)`
+ `find(Iter first, Iter last, const _Tp& val)`
+ `find(Iter first, Iter last const _Tp& val, _Pred pred, tag)`
+ `find_first_of`: 在第一个集合中找第二个集合中任意一个第一次出现的位置
+ `find_end`: 找第二个集合在第一个集合中最后一次出现的位置，和 `search` 对应
+ `adjacent_find(ForwardIter first, Forward last)`: 返回连续相邻相同的迭代器(相同的第一个)
  + 支持第三个参数是 `_BinaryPredicate`
+ `count(Iter first, Iter last, const _Tp& val)`
+ `count_if(Iter first, Iter last, _Predicate pred)`
  + 支持两种类型，还有一种是额外增加一个输出参数，`_Size_type& __n`
+ `search(Iter first1, Iter first2, Iter first2, Iter last2)`
  + 从前面的序列中找后面的序列
+ `search_n(Iter first, Iter last, _Integer _count, const _Tp& val)`
  + 查找连续出现 `n` 次的位置
+ `swap_ranges(Iter first1, Iter last1, Iter first2)`
  + 调用 `iter_swap` 来交换 `iterator` 中的内容
+ `transform(Iter first, Iter last, Iter output, _Predicate pred)`
+ `transform(Iter first1, Iter last1, Iter first2, Iter output, _BinaryPredicate pred)`
+ `generate(Iter first, Iter last, _Generator _gen)`
+ `generate_n(Iter first, _Size n, _Generator _gen)`
+ `replace(Iter first, Iter last, const _Tp& old_value, const _Tp& new_value)`
+ `replace_if(Iter first, Iter last, _Predicate pred, const _Tp& new_value)`
+ `replace_copy_if(Iter first, Iter last, Iter output, _Predicate pred, const _Tp& new_value)`
+ `remove_copy(Iter first, Iter last, Iter output, const _Tp& value)`
  + 只复制不同的值
+ `remove_copy_if(Iter first, Iter last, Iter output, _Predicate pred)`
+ `remove(Iter first, Iter last, const _Tp& value)`
+ `remove_if(Iter first, Iter last, _Predicate pred)`
+ 去重相关：前提是元素已经是有序的
  + `unique_copy(Iter first, Iter last, Iter output)`
  + `unique_copy(Iter first, Iter last, _BinaryPredicate _pred)`
  + `unique(Iter first, Iter last)`
  + `unique(Iter first, Iter last, _BinaryPredicate _pred)`
+ 反转: 对于 `random_access_iterator` 会直接 `<` 比较，其它使用 `==`
  + `reverse(Iter first, Iter last)`
  + `reverse_copy(Iter first, Iter last, Iter output)`
+ `rotate_copy`
+ `rotate`
  + 默认是进行 left rotate，如果想进行 right rotate，可以利用 `rbegin` 和 `rend` 来进行
+ `random_shuffle`
+ `random_sample`
+ `random_sample_n`
+ `equal_range`: 判断一个集合全是一个数
+ 二分查找
  + `binary_search`
  + `lower_bound`
  + `upper_bound`
+ `inplace_merge`
+ set 相关
  + `includes`
  + `set_union`
  + `set_difference`
  + `set_symmetric_difference`
  + `set_intersection`
+ `partition`
+ `stable_partition`
+ `partial_sort`: `first` 和 `middle` 之间元素有序
+ `partial_sort_copy`
+ `sort`: 插入和排序和快速排序结合
+ `stable_sort`: 相同元素位置保持不变
+ `max_element`
+ `min_element`
+ `nth_element`: 第 n 个 iterator 对应位置正确
+ `prev_permutation`
+ `next_permutation`
+ `is_heap(Iter first, Iter last)`
+ `is_heap(Iter first, Iter last, _StrictWeakOrdering _cmp)`
+ `is_sorted(Iter first, Iter last)`
+ `is_sorted(Iter first, Iter last, _StrictWeakOrdering _cmp)`
+ `merge(Iter f1, Iter l1, Iter f2, Iter l2, Iter result)`
+ `inplace_merge(Iter f, Iter m, Iter l)`


<a id="notes"></a>

### 一些 notes

+ `find` 和 `find_if` 当 `tag` 是 `random_access_iterator_tag` 时都采用了 `unloop` 的思想，
会把循环拆成 4 的倍数。最后再处理剩余的次数。
+ 对于 `OutputIter` 和 `RadomAccessIter` 两种迭代器，其比较的方式不一样
+ 最大公约数算法：`m % n == 0, return n，else old_n = n;n = m % n , m = old_n`
+ `random_shuffle` 采用了 `knuth shuffle` 原理
+ `sort` 使用插入排序和排序排序结合，当元素少时(16)直接采用插入排序，递归调用最后一层使用 `partial_sort`
其原理是 heap sort
  + 如果实现自定义的 `_Compare`，`_Compare(lhs, rhs)` 返回 `true` 的场景不能包括等于号。因为会影响
`partition` 方法对于数组的划分。

#### left and right rotate

```cpp
#include <iostream>
#include <string>
#include <vector>
#include <iterator>
#include <algorithm>

using namespace std;

template<typename T>
std::ostream& operator<<(std::ostream& os, const std::vector<T>& vec)
{
    for (auto& el : vec)
    {
        os << el << ' ';
    }
    return os;
}

int main()
{
    vector<int> a{1,2,3,4,5};
    vector<int> bb{1,2,3,4,5};
    auto b = a.rbegin();
    auto m = b;
    advance(m, 3);
    auto e = a.rend();
    rotate(b, m, e);
    copy(a.begin(), a.end(), ostream_iterator<int>(cout, ","));
    rotate(bb.begin(), bb.begin() + 3, bb.end());
    copy(bb.begin(), bb.end(), ostream_iterator<int>(cout, ","));
}
```

you can test [here](http://coliru.stacked-crooked.com/)

<a id="sort"></a>

### sort 原理

`sort` 这里我们主要讲 4 个东西：

+ `partition`
  + 根据某个准则来将数据进行切分
+ `partial_sort`
  + 利用 heap 来完成排序
+ `sort`
  + 不是稳定的排序，即元素相同，位置可能会发生变化
+ `stable_sort`

#### partition

`partition` 针对 `_ForwardIter` 和 `_BidirectionalIter` 有两种方法

+ `_ForwardIter`: 类似于 `remove` 中的方法
+ `_BidirectionalIter`: 采用双端交换的方法

`stable_partition` 递归调用：

+ 当长度小于 buffer size 时，会使用 buffer 来做 `partition`
+ 递归调用，`rotate`

递归分为 4 段：

+ part1
+ part2
+ part3
+ part4

最后把 part2 和 part3 进行交换。

#### sort

+ `__depth_limit`: 递归的深度
+ 当 `__depth_limit = 0` 时，会直接排序这部分元素

```cpp
template <class _RandomAccessIter, class _Tp, class _Size>
void __introsort_loop(_RandomAccessIter __first,
                      _RandomAccessIter __last, _Tp*,
                      _Size __depth_limit)
{
  while (__last - __first > __stl_threshold) {
    if (__depth_limit == 0) {
      partial_sort(__first, __last, __last);
      return;
    }
    --__depth_limit;
    _RandomAccessIter __cut =
      __unguarded_partition(__first, __last,
                            _Tp(__median(*__first,
                                         *(__first + (__last - __first)/2),
                                         *(__last - 1))));
    __introsort_loop(__cut, __last, (_Tp*) 0, __depth_limit);
    __last = __cut;
  }
}
```

<a id="merge"></a>

### merge 原理

`merge` 这里主要将 3 个东西：

+ merge with buffer
+ merge without buffer
+ directions of merge: foward and backward

#### inplace_merge

+ `__merge_without_buffer`
+ `__merge_adaptive`
  + 和前者的核心逻辑一致，只是在 buffer 可用时，直接调用 `merge` 或者 `__merge_backward`

```cpp
template <class _BidirectionalIter, class _Distance>
void __merge_without_buffer(_BidirectionalIter __first,
                            _BidirectionalIter __middle,
                            _BidirectionalIter __last,
                            _Distance __len1, _Distance __len2) {
  if (__len1 == 0    __len2 == 0)
    return;
  if (__len1 + __len2 == 2) {
    if (*__middle < *__first)
      iter_swap(__first, __middle);
    return;
  }
  _BidirectionalIter __first_cut = __first;
  _BidirectionalIter __second_cut = __middle;
  _Distance __len11 = 0;
  _Distance __len22 = 0;
  if (__len1 > __len2) {
    __len11 = __len1 / 2;
    advance(__first_cut, __len11);
    __second_cut = lower_bound(__middle, __last, *__first_cut);
    distance(__middle, __second_cut, __len22);
  }
  else {
    __len22 = __len2 / 2;
    advance(__second_cut, __len22);
    __first_cut = upper_bound(__first, __middle, *__second_cut);
    distance(__first, __first_cut, __len11);
  }
  _BidirectionalIter __new_middle
    = rotate(__first_cut, __middle, __second_cut);
  __merge_without_buffer(__first, __first_cut, __new_middle,
                         __len11, __len22);
  __merge_without_buffer(__new_middle, __second_cut, __last, __len1 - __len11,
                         __len2 - __len22);
}
```

merge 两端有序的数组：[first, middle), [middle, last)

+ 先将前部分拆成两端[first, first\_cut), [first\_cut, middle)
+ 然后将后部分拆成两段，但是根据 `first_cut` 的值来切分：[middle, second\_cut), [second\_cut, last)

然后将 [first\_cut, middle), 与 [middle, second\_cut) 进行 `rotate`。然后递归 merge 前部分和后部分。

本文完
