---
layout: post
title: Fixed size queue
categories: [blog, algorithm]
tags: [dailycodingproblem, twitter]
hidden: true
---

+ toc
{:toc}

### Problem

This problem was asked by Twitter.

You run an e-commerce website and want to record the last `N` order ids in a log.
Implement a data structure to accomplish this, with the following API:

`record(order_id)`: adds the `order_id` to the log
`get_last(i)`: gets the ith last element from the log.
`i` is guaranteed to be smaller than or equal to `N`.
You should be as efficient with time and space as possible.

### Solution

```cpp
#include <iostream>
#include <deque>

using namespace std;

typedef int OrderIdType;

class FixedSizeQueue {
public:
    FixedSizeQueue(const int N): n_(N) {}

    void Push(OrderIdType order_id) {
        if (_q.size() == n_) {
            _q.pop_front();
        }
        _q.push_back(order_id);
    }

    OrderIdType Get(int index) {
        return *(next(begin(_q), n_ - index));
    }

    const int size() {
        return n_;
    }

    void record(OrderIdType order_id) { Push(order_id); }
    OrderIdType get_last(int index) { return Get(index); }
private:
    deque<OrderIdType> _q;
    const int n_;

};

int main() {

    FixedSizeQueue q(2);
    for (int i = 0; i < 10; i++) {
        q.record(i);
    }
    cout << "Size: " << q.size() << endl;
    cout << "Last 1 = " << q.get_last(1) << endl;
    cout << "Last 2 = " << q.get_last(2) << endl;
    return EXIT_SUCCESS;
}
```
