---
layout: post
title: Merge interval and Insert interval
categories: [blog, algorithm]
tags: [leetcode]
redirect_from:
 - /algorithm/leetcode-interval
---

+ [题目](#problem)
+ [解法](#solution)
  + [思路](#way)
  + [代码](#code)


<a id="problem"></a>

### 题目

#### Merge interval

Given a collection of intervals, merge all overlapping intervals.

**Example 1:**

> Input: [[1,3],[2,6],[8,10],[15,18]]
>
> Output: [[1,6],[8,10],[15,18]]
>

Explanation: Since intervals [1,3] and [2,6] overlaps, merge them into [1,6].

**Example 2:**

> Input: [[1,4],[4,5]]
>
> Output: [[1,5]]

Explanation: Intervals [1,4] and [4,5] are considered overlapping.

#### Insert interval

Given a set of non-overlapping intervals, insert a new interval into the intervals (merge if necessary).

You may assume that the intervals were initially sorted according to their start times.

**Example 1:**

> Input: intervals = [[1,3],[6,9]], newInterval = [2,5]
>
> Output: [[1,5],[6,9]]

**Example 2:**

> Input: intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
>
> Output: [[1,2],[3,10],[12,16]]

Explanation: Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].


<a id="solution"></a>

### 解法

Merge interval，首先需要对所有的区间进行排序，排序的准则：

+ 先判断区间左侧是否关系：较小者排序在前
+ 如果左边界相等，根据右边界决定关系，但是这里将右侧大的往前，其实不重要

然后就遍历数组，进行合并即可：

+ 前面区间和当前区间没有交集，直接将前面区间放入结果
+ 有交集，则进行合并

整体复杂度是：`O(NlogN)`

Insert interval: 这一题可以偷懒，利用 merge interval 来实现同样的目的。即：

+ 将新区间插入，排序
+ merge

但是这种做法没有充分利用原来区间就已经有序的条件。插入一个新区间，主要就是判断新区间在原来区间中的
位置。

> [], [], [], ---, [], [], [], --- [], []
>
> [], [], [---], [], [], [] --- [], []
>
> [], [], [], ---, [], [], [---], [], []
>
> [], [], [---], [], [], [---], [], []

上图中的 dash 线表示新区建的左侧和右侧，它与原区间列表存在上述四种关系。对于上述四种关系，我们对于
dash 线前和 dash 线后的区间可以直接复制到结果中，中间直接和新区间 merge 即可。

那么中关系怎么查找呢？可以利用原来数组就是有序的前提进行二分查找。整体复杂度在 `O(N)`


<a id="way"></a>

#### 思路

+ 排序
+ 二分查找边界

<a id="code"></a>

#### 代码

```cpp
class Solution {
private:
    typedef vector<int> V;
    typedef vector<V> VV;
    struct Comp {
        bool operator()(vector<int>& lhs, vector<int>& rhs) {
            if (lhs[0] != rhs[0]) return lhs[0] < rhs[0];
            return lhs[1] < rhs[1];
        }
    };
public:
    vector<vector<int>> merge(vector<vector<int>>& intervals) {
        sort(intervals.begin(), intervals.end(), Comp());
        int size = intervals.size();
        VV result;
        if (size == 0) return result;
        auto prev = intervals[0];
        for (int i = 1; i < size; ++i) {
            auto& a = intervals[i];
            if (prev[1] < a[0]) {
                result.push_back(prev);
                prev = a;
            } else {
                // prev[1] >= a[0]

                prev[1] = max(prev[1], a[1]);
            }
        }
        result.push_back(prev);
        return result;
    }
};

class Solution {
private:
    typedef vector<int> V;
    typedef vector<V> VV;

    struct Comp {
        bool operator()(vector<int>& lhs, vector<int>& rhs) {
            if (lhs[0] != rhs[0]) return lhs[0] < rhs[0];
            return lhs[1] < rhs[1];
        }
    };


public:
    vector<vector<int>> insert1(vector<vector<int>>& intervals, vector<int>& newInterval) {
        intervals.push_back(newInterval);
        sort(intervals.begin(), intervals.end(), Comp());
        int size = intervals.size();
        VV result;
        auto prev = intervals[0];
        for (int i = 1; i < size; ++i) {
            auto& a = intervals[i];
            if (prev[1] < a[0]) {
                result.push_back(prev);
                prev = a;
            } else {
                // prev[1] >= a[0]

                prev[1] = max(prev[1], a[1]);
            }
        }
        result.push_back(prev);
        return result;
    }
    vector<vector<int>> insert(vector<vector<int>>& intervals, vector<int>& newInterval) {
        VV result;
        int size = intervals.size();
        if (size == 0) {
            result.push_back(newInterval);
            return result;
        }

        // corner case

        if (newInterval[1] < intervals[0][0]) {
            result.push_back(newInterval);
            copy(intervals.begin(), intervals.end(), back_inserter(result));
            return result;
        } else if (newInterval[0] > intervals[size-1][1]) {
            copy(intervals.begin(), intervals.end(), back_inserter(result));
            result.push_back(newInterval);
            return result;
        }

        int low = 0;
        int high = size;
        int target = newInterval[0];
        int pos_b = -1;
        while (low < high) {
            int mid = (high - low) / 2 + low;
            auto& h = intervals[mid];
            if (h[0] <= target && h[1] >= target) {
                pos_b = mid; break;
            } else if (h[1] < target) {
                low = mid + 1;
            } else if (h[0] > target) {
                high = mid;
            }
        }
        int low_b = low;
        target = newInterval[1];
        low = 0; high = size;
        int pos_e = -1;
        while (low < high) {
            int mid = (high - low) / 2 + low;
            auto& h = intervals[mid];
            if (h[0] <= target && h[1] >= target) {
                pos_e = mid; break;
            } else if (h[1] < target) {
                low = mid + 1;
            } else if (h[0] > target) {
                high = mid;
            }
        }
        int low_e = low;
        if (pos_e == -1 && pos_b == -1) {
            auto beg = intervals.begin();
            auto end = intervals.begin();
            advance(end, low_b);
            copy(beg, end, back_inserter(result));
            result.push_back(newInterval);
            end = intervals.end();
            advance(beg, low_e);
            copy(beg, end, back_inserter(result));
        } else if (pos_b == -1) {
            auto beg = intervals.begin();
            auto end = intervals.begin();
            advance(end, low_b);
            copy(beg, end, back_inserter(result));
            newInterval[1] = intervals[pos_e][1];
            result.push_back(newInterval);
            advance(beg, min(pos_e + 1, size));
            end = intervals.end();
            copy(beg, end, back_inserter(result));
        } else if (pos_e == -1) {
            auto beg = intervals.begin();
            auto end = intervals.begin();
            advance(end, pos_b);
            copy(beg, end, back_inserter(result));
            newInterval[0] = intervals[pos_b][0];
            result.push_back(newInterval);
            advance(beg, low_e);
            end = intervals.end();
            copy(beg, end, back_inserter(result));

        } else {
            auto beg = intervals.begin();
            auto end = intervals.begin();
            advance(end, pos_b);
            copy(beg, end, back_inserter(result));
            newInterval[0] = intervals[pos_b][0];
            newInterval[1] = intervals[pos_e][1];
            result.push_back(newInterval);
            advance(beg, min(pos_e + 1, size));
            end = intervals.end();
            copy(beg, end, back_inserter(result));
        }
        return result;
    }
};

```

本文完
