---
layout: post
title: Lower bound and upper bound of set/map
categories: [blog, stl]
tags: [cpp]
hidden: true
---

STL's map/set/multimap/multiset is an ordered container which compares to `unordered_map` and
`unordered_set`. So there are special methods which implemented due to the order. `multiset`
and `multimap` allow repeated elements. Its `erase` method is a little different.

+ toc
{:toc}

### Introduction

`set` and `map` are implemented using [Red-Black Tree](https://en.wikipedia.org/wiki/Red%E2%80%93black_tree).
They are sorted containers. If we traverse it from begin to end, we will get a sorted collections
according the key type.

So if we want to maintain a sorted range, we can use them. But if we want a faster insert and
access of the data, the unordered versions(`unordered_set` and `unordered_map`) are
suggested.

### Search and find

+ `lower_bound`: Find the first number which is `>=` target
+ `upper_bound`: Find the first number which is `>` target
+ `equal_range`: Range between(`lower_bound`, `upper_bound`)
+ `find`: Find the specific target, (C++ 20 intoduces `contains`)

### Delete elements

We can delete an element using `erase`. But when it comes to `multiset` or `multimap`,
it is a little different.

+ `erase(iterator pos)`
+ `erase(iterator start, iterator end)`
+ `erase(key_type key)`

When we only specify the key, it will delete all the keys instead of deleting only one
element.

In [220. Contains Duplicate III](https://leetcode.com/problems/contains-duplicate-iii/),
we need to maintain a range which is sorted. When the size of the set is larger than
required, we need to delete the head element.

```cpp
// 220. Contains Duplicate III
// https://leetcode.com/problems/contains-duplicate-iii/
class Solution {
public:
    bool containsNearbyAlmostDuplicate(vector<int>& nums, int k, int t) {
        int size = nums.size();
        if (k == 0 || size < 2) return false;
        multiset<int> s;
        s.insert(nums[0]);
        for (int i = 1; i < size; ++i) {
            auto l = s.lower_bound(nums[i]);
            auto r = prev(l);


            if (l != s.end() && (abs(*l - (long long)nums[i])) <= t) return true;
            if (r != s.end() && (abs(*prev(l) - (long long)nums[i])) <= t) return true;

            if (s.size() == k) {
                // We cannot directly delete: s.erase(nums[i-k]);
                auto ite = s.find(nums[i-k]);
                s.erase(ite);
            }

            s.insert(nums[i]);
        }
        return false;
    }
};
```

# Related

+ [Compare in set and map](/blog/stl/cpp-set-compare.html)
