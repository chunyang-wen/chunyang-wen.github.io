---
title: Implementation of A star algorithm
layout: post
category: 
- algorithms
tags:
- a-star
- c++
---

a\* 算法在人工智能领域应用比较广泛。这几天在USTC ACM上刷problem 1012，题中需要解决8-puzzle问题，有两种解法，一种是BFS，另外一种就是a\*算法。之前在Java上实现过，但是当时是利用Princeton的一个类：MinPQ，最小的优先级队列。

在C++中，其实也有priority_queue。这个是一个接口封装，底层可以使用vector或者deque实现。[priority_queue](http://www.sgi.com/tech/stl/priority_queue.html)

    priority_queue<T, Sequence, Compare>

其中T表示储存值的类型，Sequence表示底层的实现方式，Compare表示比较函数。这里需要注意的是，默认priority_queue是最大堆。

网上很多声音说这个优先级队列无法满足需求，因为无法满足动态修改优先级队列中的元素。不知道为什么priority_queue**不提供迭代器**，导致无法访问其内部元素。在a\*算法中在某些场景中需要更新队列中的元素。

其实STL的算法中提供了三个函数，push_heap，pop_heap，make_heap。利用这三个函数，外加一个**仿函数**即可实现一个最小优先级队列。

    struct Compare {
		bool operatro()(const Type &lhs, const Type &rhs)
		{
			//....
		}
	};

	make_heap(sequence.begin(), sequence.end(), Compare());

	sequence.push_back(value);
	push_heap(sequence.begin(), sequence.end(), Compare());

	pop_heap(sequence.begin(), sequence.end(), Compare());
	sequence.pop_back();

具体代码在：[a\* C++ implementation](https://github.com/chunyang-wen/code-practice/blob/master/USTC-ACM-Prob1012.cpp)

本文完
