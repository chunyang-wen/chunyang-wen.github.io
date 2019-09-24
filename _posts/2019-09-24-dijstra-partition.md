---
layout: post
title: Dijkstra's 3-way quick sort
categories: [blog, algorithm]
tags: [algorithm]
---

Quick-sort is one of the greatest inventions. Most of the time, its time complexity is O(nlogn).
However, when the input array contains lots of duplicates, the performance will drop. For example,

```cpp
vector<int> a{1, 1, 1, 1}
```

The elements of the array `a` are all the same. A naive quick-sort algorithm will have a O(n^2) time
complexity.

I have implemented the Dijkstra 3-way quick-sort manually.

```cpp
typedef pair<int, int> IntPair;
IntPair partition(vector<int>& arr, int start, int end) {
    if (start >= end) return make_pair(end, end);
    // select the first element as the pivot

    int i = start;
    int j = start;
    int k = end;
    int pivot = arr[i];
    while (j < k) {
        if (arr[j] == pivot) {
            ++j;
        } else if (arr[j] < pivot) {
            swap(arr[i], arr[j]);
            ++i;
            ++j;
        } else {
            swap(arr[j], arr[k-1]);
            --k;
        }
    }
    return make_pair(i, j);

}
```

Actually STL has already supported this kind of operation. You can refer to [partition](https://en.cppreference.com/w/cpp/algorithm/partition)
for more details.


```cpp
void quick_sort(vector<int>& arr, int start, int end) {
    if (start >= end) return make_pair(end, end);
    auto beg = arr.begin(); advance(beg, start);
    auto end = arr.begin(); advance(end, end);
    int pivot = *beg;
    auto middle1 = std::partition(beg, end, [](int x) {return x < pivot;});
    auto middle2 = std::partition(middle1, end, [](int x){return x <= pivot;});
    // middle1 and middle2 are the start and end of the array with same element;

    quick_sort(arr, start, distance(middle1, arr.begin()));
    quick_sort(arr, distance(middle2, arr.begin()), end);
}
```

Cool! Let's learn more about STL.


+ [QuickSort Dijkstra 3-Way Partitioning: why the extra swapping?](https://cs.stackexchange.com/questions/22389/quicksort-dijkstra-3-way-partitioning-why-the-extra-swapping)
+ [partition](https://en.cppreference.com/w/cpp/algorithm/partition)
