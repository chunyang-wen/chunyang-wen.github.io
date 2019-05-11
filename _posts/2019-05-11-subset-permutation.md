---
layout: post
title: Subsets and Permutations
categories: [algorithm]
tags: [leetcode]
---

+ [题目](#problem)
+ [解法](#solution)
  + [思路](#way)
  + [代码](#code)


<a id="problem"></a>

### 题目

#### Subsets

Given a set of distinct integers, nums, return all possible subsets (the power set).

Note: The solution set must not contain duplicate subsets.

#### Permutation

Given a collection of distinct integers, return all possible permutations.

<a id="solution"></a>

### 解法

在面试中会经常遇到的一类题目是 `subset` 和 `permutation` 问题。前者是组合，后者是排列。由于需要遍历
出所有的结果，其复杂度：

+ 组合：`2^n`
+ 排列：`n!`

题目一般分为两个等级，这个数组中是否有重复元素，一般对于没有重复元素的方法比较好解。

<a id="way"></a>

#### 思路

**对于组合**

组合一般会要求其所有的子集（包括空集合），也称之为 `power set`。例如对于 `[1,2]`，其所有子集为：

`[], [1], [2], [1,2]`

如果没有出现重复，则我们可以用一个 index 记录当前开始的位置，对于当前位置的元素，我们可以采取：

+ 取当前元素
+ 不取当前元素

然后增加这个 index，后续递归去调用。

如果存在重复元素怎么处理？这里的思路将数分组，形成类似的 bag 的东西。我们在取数构造组合时，每次都从
 bag 去取，对于每一个 bag，有两种处理方式：

+ 不取，直接跳过这个 bag
+ 取，挨个取

这种思路也可以用于解决第一种，第一种是这种方式的一个特殊形式，即每个 bag 中只有一个元素。

**对于排列**

主要参考 [排列](http://rangerway.com/way/algorithm-permutation-combination-subset)

其思路是类似于 DFS 的策略，先选一个数，然后继续选。目的是实现如下结果：

`1, 2, 3`, `1, 3, 2`, `2, 1, 3`, `2, 3, 1`, `3, 2, 1`, `3, 1, 2`

每一个元素作为开始元素，其后面的元素都实现全排列。如果存在重复元素时，在递归调用的循环部分，需要跳
过已经交换过的元素。

<a id="code"></a>

#### 代码

```cpp

class Solution {
private:
    void subsets(vector<int>& nums, vector<vector<int>>& result, vector<int>& cur, int k, int pos) {
        if (cur.size() == k) {
            result.push_back(cur);
            return;
        }
        int size = nums.size();
        for (int i = pos; i < size; ++i) {
            cur.push_back(nums[i]);
            subsets(nums, result, cur, k, i+1);
            cur.pop_back();
        }
    }
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        vector<vector<int> > result;
        int size = nums.size();
        result.emplace_back(vector<int>());
        vector<int> cur;
        for (int i = 1; i <= size; ++i) {
            subsets(nums, result, cur, i, 0);
        }
        return result;
    }
};

class Solution {
typedef vector<vector<int>> VV;
typedef map<int, int> Bag;
private:
    void subsets(Bag& bags, VV& result, vector<int>& cur, int k) {

        if (cur.size() == k) {
            result.push_back(cur);
            return;
        }

        if (bags.empty()) return;
        auto iter = bags.begin();
        int bag_num = (*iter).first;
        int bag_size = (*iter).second;
        bags.erase(iter);

        // with current bag;
        int i = 0;
        for (; i < bag_size;) {
            cur.push_back(bag_num);
            ++i;
            if (cur.size() > k) break;
            subsets(bags, result, cur, k);
        }

        // without current bag;
        cur.resize(cur.size() - i);
        subsets(bags, result, cur, k);

        bags[bag_num] = bag_size;

    }
public:
    vector<vector<int>> subsets(vector<int>& nums) {
        VV result;
        result.emplace_back(vector<int>());
        vector<int> cur;

        // build bag
        map<int, int> bags;
        for(auto num: nums) {
            bags[num]++;
        }
        int size = nums.size();
        for (int i = 1; i <= size; ++i) {
            subsets(bags, result, cur, i);
        }
        return result;
    }
};

```

```cpp
class Solution {
public:
    typedef vector<vector<int> > VV;
    typedef vector<int> V;

private:
    void permute(V& nums, VV& result, int start) {
        int size = nums.size();
        if (start == size) {
            result.push_back(nums);
            return;
        }
        for (int i = start; i < size; ++i) {
            swap(nums[start], nums[i]);
            permute(nums, result, start + 1);
            swap(nums[i], nums[start]);
        }
    }
public:
    vector<vector<int>> permute(vector<int>& nums) {
        VV result;
        permute(nums, result, 0);
        return result;
    }
};

class Solution {
public:
    typedef vector<int> V;
    typedef vector<V> VV;
    typedef set<int> Set;

private:
    void permuteUnique(V& nums, VV& result, int start) {
        int size = nums.size();
        if (start == size) {
            result.push_back(nums);
            return;
        }
        Set s;
        for (int i = start; i < size; ++i) {
            if (s.insert(nums[i]).second) {
                swap(nums[i], nums[start]);
                permuteUnique(nums, result, start + 1);
                swap(nums[i], nums[start]);
            }
        }
    }

public:
    vector<vector<int>> permuteUnique(vector<int>& nums) {
        VV result;
        permuteUnique(nums, result, 0);
        return result;
    }
};
```

本文完
