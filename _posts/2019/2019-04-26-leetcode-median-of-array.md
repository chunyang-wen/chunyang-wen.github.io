---
layout: post
title: Median of two sorted arrays
categories: [blog, algorithm]
tags: [leetcode]
---

+ [题目](#problem)
+ [解法](#solution)
  + [思路](#way)
  + [代码](#code)


<a id="problem"></a>

### 题目

There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

You may assume nums1 and nums2 cannot be both empty.

**Example 1:**

> nums1 = [1, 3]
>
> nums2 = [2]

> The median is 2.0

**Example 2:**

> nums1 = [1, 2]
> nums2 = [3, 4]

> The median is (2 + 3)/2 = 2.5

<a id="solution"></a>

### 解法

<a id="way"></a>

#### 思路

需要充分利用两个数组已经有序的条件。如果我们使用类似于 merge 的方法，可以在 O(m+n) 时间范围内解决
问题。如果我们利用类似于二分查找的算法，可以将复杂度降低到对数时间水平。

注意一些 corner case：

+ 每次都将需要查找的 target 降低一半
+ 当其中一个为空时，我们直接返回另外一个数组里面对应的元素即可

<a id="code"></a>

#### 代码

```cpp
class Solution {
    double findMedianSortedArraysHelper(
        vector<int>& nums1, int s1, int e1,
        vector<int>& nums2, int s2, int e2, int target) {
        if (e1 - s1 > e2 - s2) {
            return findMedianSortedArraysHelper(nums2, s2, e2, nums1, s1, e1, target);
        }
        if (s1 >= e1) return nums2[s2 + target];
        if (s2 >= e2) return nums1[s1 + target];
        if (target == 0) return nums1[s1] < nums2[s2] ? nums1[s1] : nums2[s2];
        int mid1 = s1 + (target - 1) / 2;
        if (mid1 >= e1) mid1 = e1-1;
        int mid2 = s2 + (target - 1) - (mid1 - s1);

        cout << "num1: " << s1 << " " << e1 << " " << mid1 << endl;
        cout << "num2: " << s2 << " " << e2 << " " << mid2 << endl;
        cout << "target: " << target << " index: " << (mid1 - s1 + mid2 - s2 + 2) << endl;

        // assert(target >= 0);

        // assert(target == (mid1 - s1 + mid2 - s2 + 2));

        if (nums1[mid1] == nums2[mid2]) return nums1[mid1];
        else if (nums1[mid1] > nums2[mid2]) {
            auto diff = mid2 - s2 + 1;
            return findMedianSortedArraysHelper(nums1, s1, e1, nums2, mid2+1, e2, target - diff);
        } else {
            auto diff = mid1 - s1 + 1;
            return findMedianSortedArraysHelper(nums1, mid1+1, e1, nums2, s2, e2, target - diff);
        }
    }
public:
    double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
        int m = nums1.size();
        int n = nums2.size();
        int sum = m + n;
        if ((sum & 0x1) == 0) {
            // even

            auto a = findMedianSortedArraysHelper(nums1, 0, m, nums2, 0, n, sum / 2);

            // cout << "A: " << a << endl;

            auto b = findMedianSortedArraysHelper(nums1, 0, m, nums2, 0, n, sum / 2 - 1);

            // cout << "B: " << b << endl;

            return (a + b) / 2.0;
        } else {
            // odd

            return findMedianSortedArraysHelper(nums1, 0, m, nums2, 0, n, sum / 2);
        }
    }
};

```

本文完
