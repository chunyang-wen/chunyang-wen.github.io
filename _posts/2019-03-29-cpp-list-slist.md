---
layout: post
title: C++ STL list and slit
categories: [blog, stl]
tags: [cpp]
---

+ [简介](#intro)
+ [单链表](#slit)
+ [双向链表](#list)
+ [总结](#summary)

<a id="intro"></a>

### 简介

STL 中提供了单向链表和双向链表。(好像单向链表并没有进入 C++ 标准)

+ `slist`
+ `list`

支持常见的操作

+ `push/pop_back`: **双向链表**
+ `push/pop_front`
+ `front`
+ `back`: **双向链表**
+ `remove`
+ `reverse`
+ `unique`
+ `merge`: 归并两个有序链表
+ `sort`: 会单独介绍，链表的 sort 是归并。STL 中的 sort 不适合链表
+ `splice`
+ `splice_after`: **单链表**
  + 这个函数的入参有点奇怪

<a id="slist"></a>

### 单链表

单向链表，顾名思义只能往一个方向去访问：每个节点含有指向下个节点的指针以及本节点所存储的元素。

```cpp
struct _Slist_node_base
{
  _Slist_node_base* _M_next;
};

template <class _Tp>
struct _Slist_node : public _Slist_node_base
{
  _Tp _M_data;
};
```

单向链表只支持 `operator++`，其实现就是移动相关的指针。在单向链表结构中存储的结构 `_M_head` 实际上
不是真正的头节点。它的下一个节点是头结点，它属于 `before_first`。单链表的插入都是在表头：

+ `push_front/pop_front`

所以如果我们需要构造一个链表的话，有点类似于栈一样，需要方向插入节点。

单向链表结构在面试中会经常遇到，例如单向列表的反转，单向链表的去重和合并。

#### 链表反转

```cpp
inline _Slist_node_base* __slist_reverse(_Slist_node_base* __node)
{
  _Slist_node_base* __result = __node;
  __node = __node->_M_next;
  __result->_M_next = 0;
  while(__node) {
    _Slist_node_base* __next = __node->_M_next;
    __node->_M_next = __result;
    __result = __node;
    __node = __next;
  }
  return __result;
}
```

#### 链表删除指定元素

这里 `_M_head` 并不是真正的头节点，这个类似于 dummy 节点的头结点会简化程序。因为我们不需要判断头
节点被删除的场景。

```cpp
template <class _Tp, class _Alloc>
void slist<_Tp,_Alloc>::remove(const _Tp& __val)
{
  _Node_base* __cur = &this->_M_head;
  while (__cur && __cur->_M_next) {
    if (((_Node*) __cur->_M_next)->_M_data == __val)
      this->_M_erase_after(__cur);
    else
      __cur = __cur->_M_next;
  }
}
```

#### 链表合并

链表的合并，假定两个链表都是各自有序的。

```cpp
 template <class _Tp, class _Alloc>
 void slist<_Tp,_Alloc>::merge(slist<_Tp,_Alloc>& __x)
 {
   _Node_base* __n1 = &this->_M_head;
   while (__n1->_M_next && __x._M_head._M_next) {
     if (((_Node*) __x._M_head._M_next)->_M_data <
         ((_Node*)       __n1->_M_next)->_M_data)
       __slist_splice_after(__n1, &__x._M_head, __x._M_head._M_next);
     __n1 = __n1->_M_next;
   }
   if (__x._M_head._M_next) {
     __n1->_M_next = __x._M_head._M_next;
     __x._M_head._M_next = 0;
   }
 }
```

`__slist_splice_after` 函数作用是什么呢？

> 其作用是将 `_first`, `_before_last` 之间的元素插入到 `__pos` 位置,
> 然后元素拼接起来

```conf
__pos->__first->__before_last->__pos.next
```

这个函数的入参有一点奇怪，不是正常的节点，而节点的上一个节点。STL 中所有区间的描述都是左闭右开的
`[first, last)`，这里的 `__before_first` 应该是某个 `slist` 的 `_M_head`，因为程序把它的下游指向
了 `__last` 节点

```cpp
inline void __slist_splice_after(_Slist_node_base* __pos,
                                 _Slist_node_base* __before_first,
                                 _Slist_node_base* __before_last)
{
  if (__pos != __before_first && __pos != __before_last) {
    _Slist_node_base* __first = __before_first->_M_next;
    _Slist_node_base* __after = __pos->_M_next;
    __before_first->_M_next = __before_last->_M_next;
    __pos->_M_next = __first;
    __before_last->_M_next = __after;
  }
}

inline void
__slist_splice_after(_Slist_node_base* __pos, _Slist_node_base* __head)
{
  _Slist_node_base* __before_last = __slist_previous(__head, 0);
  if (__before_last != __head) {
    _Slist_node_base* __after = __pos->_M_next;
    __pos->_M_next = __head->_M_next;
    __head->_M_next = 0;
    __before_last->_M_next = __after;
  }
}
```

#### 单链表排序

+ 构建 `slist __counter[64]` 个链表
+ 合并上面生成的链表

`__counter[0]` 存储一个节点，`__counter[1]` 存储两个节点， `__counter[n]` 存储 `2^n` 次方个节点。
每次都从原始的节点列表中合并掉 `2^n` 个节点。

具体执行流程：

+ 每次通过 `__slist_splice_after` 往 carry 中增加一个节点
+ 每次往 `__counter[0]` 中插入节点，每次增加一个 level 后，前面的 level 都会被清空

例如当前状态 `__counter[2]` 中存储了 4 个节点，`__counter[0]` 和 `__counter[1]` 都是空。这个时候会
先去填满 `__counter[0]`，然后填满 `__counter[1]`，清空 `__counter[0]`，然后填满 `__counter[0]`，这个
时候再到达一个节点，会不断往上合并，`__counter` 状态是 `[1,2,4,0,0...0]`。然后会不断合并，最终生成
`[0,0,0,8,0...0]`

```cpp
 template <class _Tp, class _Alloc>
 void slist<_Tp,_Alloc>::sort()
 {
   if (this->_M_head._M_next && this->_M_head._M_next->_M_next) {
     slist __carry;
     slist __counter[64];
     int __fill = 0;
     while (!empty()) {
       __slist_splice_after(&__carry._M_head,
                            &this->_M_head, this->_M_head._M_next);
       int __i = 0;
       while (__i < __fill && !__counter[__i].empty()) {
         __counter[__i].merge(__carry);
         __carry.swap(__counter[__i]);
         ++__i;
       }
       __carry.swap(__counter[__i]);
       if (__i == __fill)
         ++__fill;
     }

     for (int __i = 1; __i < __fill; ++__i)
       __counter[__i].merge(__counter[__i-1]);
     this->swap(__counter[__fill-1]);
   }
 }
```

<a id="list"></a>

#### 双向链表

双向链表相对于单向链表，增加了前向的节点，支持的移动方式会增加一种，向前向后都可以。

```cpp
struct _List_node_base {
  _List_node_base* _M_next;
  _List_node_base* _M_prev;
};

template <class _Tp>
struct _List_node : public _List_node_base {
  _Tp _M_data;
};
```

双向链表也有一个 dummy 节点，这个 dummy 节点再最开始时指向自己，所以 `empty()` 的实现如下：

```cpp
bool empty() const { return _M_node->_M_next == _M_node; }
```

> \<\<STL 源码剖析\>\>中说，这个会节约一个 Node 的存储空间

#### splice

+ `void splice(iterator __position, list& __x)`
+ `void splice(iterator __position, list&, iterator __i)`
+ `void splice(iterator __position, list&, iterator __first, iterator __last)`

主要依赖 `transfer` 实现，`transfer` 功能是要将 `__position` 位置的元素替换为`[__first, __last]`。
这个过程中维护 `__position` 和 `__first`、`__last` 前序和后序之间的关系。

```cpp
void transfer(iterator __position, iterator __first, iterator __last) {
  if (__position != __last) {
      /* Remove [first, last) from its old position. */
      __last._M_node->_M_prev->_M_next     = __position._M_node;
      __first._M_node->_M_prev->_M_next    = __last._M_node;
      __position._M_node->_M_prev->_M_next = __first._M_node;

      /* Splice [first, last) into its new position. */
      _List_node_base* __tmp      = __position._M_node->_M_prev;
      __position._M_node->_M_prev = __last._M_node->_M_prev;
      __last._M_node->_M_prev     = __first._M_node->_M_prev;
      __first._M_node->_M_prev    = __tmp;
  }
}
```


<a id="summary"></a>

#### 总结

STL 中很多通用的算法是不能直接用在链表上。一般这些算法会要求 `random_access_iterator`。STL 的链表
实现中的排序、反转对于面试中有很多借鉴意义。


本文完
