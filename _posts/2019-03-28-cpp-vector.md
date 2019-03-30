---
layout: post
title: C++ STL Vector
categories: [cpp]
tags: [cpp, STL, vector]
---

+ [简介](#intro)
+ [实现细节](#implementation-details)
  + [增加元素的操作](#add-ele)
  + [删除元素的操作](#del-ele)
+ [其它操作](#other-ops)

<a id="intro"></a>

### 简介

C++ STL Vector 是经典的连续存储空间的数据。它有两个模板参数：

+ 存储类型: 所存储数据的类型
+ `_Alloc`: 表示其所使用的空间分配器，一般情况下不需要增加这个参数，除非有自定的需求

`vector` 的实现比较简单，其实也不简单。它考虑了很多的性能优化，例如对于简单类型复制构造使用更高效的
`uninitialized_copy/fill`; 扩张内存时，其内存扩张策略；兼容不同的 allocator （这部分工作感觉很多容器都会考虑）

<a id="implementation-details"></a>

### 实现细节

+ `_M_start`
+ `_M_finish`
+ `_M_end_of_storage`

这三个指针指向的是当前 vector 存储的空间和位置信息，这些在迭代器部分提供非常方便的实现。例如 `begin`
可以返回 `_M_start`，`size()` 实现为 `end() - begin()`，本质还是指针间的运算。

<a id="add-ele"></a>

#### 增加元素的操作

+ `push_back`
+ `insert`
  + `insert(iterator __pos)`
    + 不知道为什么这个函数没有调用下面的函数来实现
  + `insert(iterator __pos, const _Tp& __x)`
  + `insert(iterator __pos, InputIterator __first, InputIterator __last)`
  + `insert(iterator __pos, size_type __n, const _Tp& __x)`

`push_back` 操作在 `_M_end_of_storage > _M_finish` 时，只需要做下移动即可。其它情况需要做内存的扩张。

```cpp
vector<_Tp, _Alloc>::_M_insert_aux(iterator __position, const _Tp& __x) {
    /* _M_finish != _M_end_of_storage */
    /* 增加 _M_finish, 然后反向复制，最后在 __position 位置插入元素*/

    /* new_size = old_size == 0 ? 1 : 2 * old_size */
    /* 复制 _M_start->__position */
    /* 复制 __position->_M_finish */
    /* 赋值 __position 位置的值 */
}
```

疑惑点：

+ 为什么要调用一下 `construct`?
  + 那部分 `_M_end_of_storage` 标记的只是内存空间，并没有初始化，所以必须先 `construct`，然后再复制
  + `else` 分支中调用了：`uninitialized_copy`，函数内部会根据情况去调用复制构造函数
+ 复制一份 `__x`: 防止变量会被覆盖吗？
  + 防止传入的引用是在 `copy_backward` 的方位之内

<a id="del-ele"></a>

#### 删除元素的操作

+ `pop_back`
+ `erase`
  + `erase(iterator __position)`
  + `erase(iterator __first, iterator __last)`

`pop_back` 的实现比较简单，标记下 `_M_finish`，然后 `destroy` 掉之前位置的元素即可。`erase` 的实现
是类似的，只不过从末位换到一个任意位置，或者区间。注意 `erase` 返回的是删除元素的下一个位置。该
返回值主要用于遍历删除。

```cpp
/* delete all elements in an array of int */

void delete_ele(vector<int> array, int target) {
    auto beg = array.begin();
    auto end = array.end();
    while (beg != end) {
        if (*beg == target) {
            beg = erase(beg);
        } else {
            ++beg;
        }
    }
}
```

<a id="other-ops"></a>

#### 其它操作

+ `assign`
  + `assign` 会替换掉整个 `vector` 的内容
  + 有直接插入值和插入一个区间两种实现
+ `swap`
  + `swap` 的实现其实比较简单，就是交换之前存储的三个状态值即可。
+ comparison
  + 比较的实现主要是实现 `==` 和 `<`。前者使用 `equal` 实现，后者是 `lexicographical_compare`

本文完
