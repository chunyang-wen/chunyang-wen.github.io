---
layout: post
title: priority queue and heap
categories: [cpp]
tags: [stl, heap, priority_queue]
---

+ [简介](#intro)
+ [heap](#heap)
+ [priority queue](#priority-queue)
+ [应用](#application)

<a id="intro"></a>

### 简介

<a id="heap"></a>

### heap

对于支持 `RandomAccessIterator` 的容器适用。默认构造最大堆。

+ `push_heap`
  + 元素放在末尾，然后 `__push_heap`
+ `pop_heap`
  + pop 元素会放在末尾，然后插入末尾的元素
+ `make_heap`
  + [0, n/2) 不断地去 `__adjust_heap`
+ `sort_heap`
  + 不断地调用 `pop_heap`

#### `__push_heap`

假定已经是一个 `heap` 了，新插入的元素在末尾，不断地和它的 `parent` 比较，如果比

+ `__value > *_parent`: 则递归往上找，当前节点替换为其 `parent` 的值
+ `__value <= *_parent`: 则停止，找到所要插入的位置，插入元素即可

```cpp
 template <class _RandomAccessIterator, class _Distance, class _Tp>
 void
 __push_heap(_RandomAccessIterator __first,
             _Distance __holeIndex, _Distance __topIndex, _Tp __value)
 {
   _Distance __parent = (__holeIndex - 1) / 2;
   while (__holeIndex > __topIndex && *(__first + __parent) < __value) {
     *(__first + __holeIndex) = *(__first + __parent);
     __holeIndex = __parent;
     __parent = (__holeIndex - 1) / 2;
   }
   *(__first + __holeIndex) = __value;
 }
```

#### `__adjust_heap`

当移除一个元素时，需要找到它的替代元素。不断找左右孩子中较大的：

+ 将移除位置不断和它孩子中较大的元素交换，直至到最后的结尾
  + 这一步确保从 `holeIndex` 到下面是满足 `heap` 的顺序结构的
+ 然后再把元素插入到末尾

```cpp
template <class _RandomAccessIterator, class _Distance, class _Tp>
void
__adjust_heap(_RandomAccessIterator __first, _Distance __holeIndex,
              _Distance __len, _Tp __value)
{
  _Distance __topIndex = __holeIndex;
  _Distance __secondChild = 2 * __holeIndex + 2;
  while (__secondChild < __len) {
    if (*(__first + __secondChild) < *(__first + (__secondChild - 1)))
      __secondChild--;
    *(__first + __holeIndex) = *(__first + __secondChild);
    __holeIndex = __secondChild;
    __secondChild = 2 * (__secondChild + 1);
  }
  if (__secondChild == __len) {
    *(__first + __holeIndex) = *(__first + (__secondChild - 1));
    __holeIndex = __secondChild - 1;
  }
  __push_heap(__first, __holeIndex, __topIndex, __value);
}
```

<a id="priority-queue"></a>

### priority queue

优先级队列实际上 `stl_heap` 中提供几种接口的一种封装。其模板有 3 个参数：
`priority_queue<_Tp, _Sequence, _Compare>`

默认情况下：

+ `_Sequence = vector`
+ `_Compare = less`

其提供的接口和 `stack` 比较类似：

+ `push`
+ `pop`
+ `top`

<a id="application"></a>

### 应用

+ 堆排序
+ 合并 K 个有序数组或者队列
+ Dijstra 算法：单源最短路径

本文完
