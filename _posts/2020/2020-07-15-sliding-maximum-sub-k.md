---
layout: post
title: Sliding maximum of range k subarray
categories: [blog, algorithm]
tags: [dailycodingproblem, google]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

Given an array of integers and a number `k`, where 1 <= `k` <= length of the array,
compute the maximum values of each subarray of length `k`.

For example, given array = [10, 5, 2, 7, 8, 7] and `k` = 3, we should get: [10, 7, 8, 8], since:

```cpp
10 = max(10, 5, 2)
7 = max(5, 2, 7)
8 = max(2, 7, 8)
8 = max(7, 8, 7)
```

Do this in `O(n)` time and `O(k)` space. You can modify the input array in-place and you do
not need to store the results. You can simply print them out as you compute them.

### Solution

+ Use a `deque` to keep track of a decreasing sequence, the length is at most `k`
+ When the first element is outside of range k, `pop_front`

#### Complexity analysis

+ Every element will only enter into and leave out the `deque` once

```cpp
#include <algorithm>
#include <iostream>
#include <deque>
#include <vector>
#include <iterator>
#include <utility>

using namespace std;

/*
 * [10, 5, 2, 7, 8, 7]
 *
 */
vector<int> maximum_sub_k(const vector<int>& arr, int k) {
    vector<int> result;
    if (arr.empty()) return result;
    deque<pair<int, int> > dq;  // <value, index>
    dq.push_back(make_pair(arr[0], 0));
    int size = arr.size();
    for (int i = 1; i < size; ++i) {
        if (i >= k) {
            result.push_back(dq.front().first);
        }
        if (dq.empty() || dq.back().first > arr[i]) {
            dq.push_back(make_pair(arr[i], i));
        } else {
            while (!dq.empty() && dq.back().first < arr[i]) dq.pop_back();
            dq.push_back(make_pair(arr[i], i));
        }
        if (i - dq.front().second >= k) dq.pop_front();
    }
    result.push_back(dq.front().first);
    return result;

}

void test(const vector<int>& arr, int k) {
    auto result = maximum_sub_k(arr, k);
    copy(begin(result), end(result), ostream_iterator<int>(cout, ","));
    cout << endl;
}


int main() {

    test({10, 5, 2, 7, 8, 7}, 3);
    test({10, 9, 8, 7, 6, 5}, 3);
    test({5,6,7,8,9,10}, 3);
    test({1,2,3,4,5,6,7}, 1);

    return 0;
}
```
