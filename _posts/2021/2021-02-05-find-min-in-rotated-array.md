---
layout: post
title: Find the minimum in a rotated array
categories: [blog, algorithm]
tags: [leetcode]
hidden: true
---

一个递增有序数组，在中间某个位置被旋转。在旋转的数组中找到最小值。

+ toc
{:toc}

网上其实有很多题解，但是一直看不明白他们为什么和正常的二分查找不一致。其实本质上就是二分查找，
只不过我们需要处理好边界条件。


### 没有重复元素

```cpp
int findMin(vector<int>& arr) {
    int start = 0, end = arr.size();
    while (start < end) {
        int mid = (end - start)/2 + start;
        if (mid > start && arr[mid] < arr[mid-1]) return arr[mid];
        else if (mid < end - 1 && arr[mid] > arr[mid+1]) return arr[mid+1];
        else {
            if (arr[start] <= arr[mid]) {
                if (arr[start] < arr[end-1]) return arr[start];
                start = mid + 1;
            } else {
                end = mid;
            }
        }
    }
    return arr[0];
}
```

### 有重复元素

```cpp
int findMin(vector<int>& arr) {
    int start = 0, end = arr.size();
    while (start < end) {
        int mid = (end - start)/2 + start;
        if (mid > start && arr[mid] < arr[mid-1]) return arr[mid];  // 1
        else if (mid < end - 1 && arr[mid] > arr[mid+1]) return arr[mid+1];  // 2
        else {
            if (arr[start] < arr[mid]) {
                if (arr[start] < arr[end-1]) return arr[start];
                start = mid + 1;
            } else if (arr[start] > arr[mid]){
                // 如果 arr[mid] 是最小值，会在 2 出的 if 匹配掉返回
                end = mid;
            } else {
                ++start;
            }
        }
    }
    return arr[0];
}
```
