---
layout: post
title: C++ STL stack, queue and deque
categories: [cpp]
tags: [queue, stack, deque]
---

+ [简介](#intro)
+ [栈](#stack)
+ [队列](#queue)
+ [双端队列](#deque)

<a id="intro"></a>

### 简介

本部分主要介绍三种容器：

+ `stack`
+ `queue`
+ `deque`

他们分别是栈，队列（FIFO）, 双端队列（两侧可以出入）。


<a id="stack"></a>

### 栈

模板参数包括两个：

+ `_Tp`: 存储数据类型
+ `_Sequence`: 底层实现的容器

`stack` 这是一个简单的包装，它主要实现接口如下：

+ `top`: 返回栈顶的元素，`_Sequence.back()`
+ `empty`: 判断栈是否是空，`_Sequence` 同名方法
+ `push`: 向栈中压入元素，`_Sequence.push_back()`
+ `pop`: 删除栈顶元素，`_Sequence.pop_back()`
+ `size`: 返回栈中元素个数，`_Sequence` 同名方法

这些都是依赖它所对应的 `_Sequence` 来实现的。默认的 `_Sequence` 是后面介绍的双端队列 `deque`

<a id="queue"></a>

### 队列

队列和栈一样，也是一个 **wrapper**。它也是对它所使用的 `_Sequence` 接口进行封装适配。

+ `front`
+ `back`
+ `push`: `_Sequence.push_back()`
+ `pop`: `_Sequence.pop_front()`
+ `empty`
+ `size`

队列默认的 `_Sequence` 是 `deque`。

<a id="deque"></a>

###  双端队列

栈和队列在默认情况都是使用 `deque` 来作为其实际的存储容器。`deque` 作为双端队列，其可以在头和尾部
进行元素的插入和删除，都是 `O(1)` 的复杂度(通常情况下，不考虑内存扩张时的复制)。

#### `deque` 的内存管理

内存管理类似于操作系统的分页（当然比操作操作系统的段页式是弱的）。在 `_Deque_iterator` 中：

+ `_M_cur`: 当前元素的指针
+ `_M_first`：当前页中头指针
+ `_M_last`：当前页中尾指针
+ `_M_node`：当前所在页的指针，是个二级指针

当移动节点跨越边界时，会调用下述函数来进行页面的切换：

```cpp
void _M_set_node(_Map_pointer __new_node) {
  _M_node = __new_node;
  _M_first = *__new_node;
  _M_last = _M_first + difference_type(_S_buffer_size());
}
```

注意在边界操作时，`_M_cur` 的变化：

+ 往后移动时，先移动 `++_M_cur`，然后判断是否跨页，然后设置 `_M_cur = _M_first`
+ 往前移动时, 先判断是否跨页，然后 `--_M_cur`

我们通过几个比较有意思的移动来看下分页管理上的一些复杂度：

求两个 `iterator` 之间的距离 `operator-`：

+ `this` 所在 `iterator` 位于 `__x` 的后面
  + 直观理解
+ `this` 所在 `iterator` 位于 `__x` 的前面
  + 这个时候，第一部分是个负值，会发现有多减掉部分指针，所以加回去

```cpp
difference_type operator-(const _Self& __x) const {
  return difference_type(_S_buffer_size()) * (_M_node - __x._M_node - 1) +
      (_M_cur - _M_first) + (__x._M_last - __x._M_cur);
}
```

快速移动 `iterator`， `operator+=`: 移动时需要注意当跨越 `page` 时需要重新设置存储 `Map` 对应的节点。

```cpp
_Self& operator+=(difference_type __n)
{
  difference_type __offset = __n + (_M_cur - _M_first);
  if (__offset >= 0 && __offset < difference_type(_S_buffer_size()))
      _M_cur += __n;
  else {
      difference_type __node_offset =
          __offset > 0 ? __offset / difference_type(_S_buffer_size())
          : -difference_type((-__offset - 1) / _S_buffer_size()) - 1;
      _M_set_node(_M_node + __node_offset);
      _M_cur = _M_first +
          (__offset - __node_offset * difference_type(_S_buffer_size()));
  }
  return *this;
}
```

`erase` : 先判断哪部分元素少，然后再决定元素的移动，`erase` 的删除是 `O(n)`

```cpp
iterator erase(iterator __pos) {
  iterator __next = __pos;
  ++__next;
  difference_type __index = __pos - _M_start;
  if (size_type(__index) < (this->size() >> 1)) {
    copy_backward(_M_start, __pos, __next);
    pop_front();
  }
  else {
    copy(__next, _M_finish, __pos);
    pop_back();
  }
  return _M_start + __index;
}
```

感兴趣地可以看下 `_M_push_back_aux`、`_M_push_front_aux` 和 `_M_insert_aux` 的实现。这些都是在页面
的边界时才会调用的代码。

本文完
