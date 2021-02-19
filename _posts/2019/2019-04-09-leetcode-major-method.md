---
layout: post
title: Majority Element I && II
categories: [blog, algorithm]
tags: [leetcode]
hidden: true
---

+ [题目](#problem)
+ [解法](#solution)
  + [思路](#way)
  + [代码](#code)


<a id="problem"></a>

### 题目

本次主要涉及 3 个题目。前两个题目是 Majority Element I 和 II，第三个是一个类似的应用。

#### Majority Element

Given an array of size n, find the majority element. The majority element is the element that appears more than ⌊ n/2 ⌋ times.

You may assume that the array is non-empty and the majority element always exist in the array.

Example 1:

> Input: [3,2,3]
>
> Output: 3

Example 2:

> Input: [2,2,1,1,1,2,2]
>
> Output: 2

#### Majority Element II

Given an integer array of size n, find all elements that appear more than ⌊ n/3 ⌋ times.

Note: The algorithm should run in linear time and in O(1) space.

Example 1:

> Input: [3,2,3]
>
> Output: [3]

Example 2:

> Input: [1,1,1,3,3,2,2,2]
>
> Output: [1,2]

#### String Compression

Given an array of characters, compress it in-place.

The length after compression must always be smaller than or equal to the original array.

Every element of the array should be a character (not int) of length 1.

After you are done modifying the input array in-place, return the new length of the array.


Follow up:
Could you solve it using only O(1) extra space?


Example 1:

> Input:
> ["a","a","b","b","c","c","c"]
>
> Output:
> Return 6, and the first 6 characters of the input array should be: ["a","2","b","2","c","3"]

Explanation:
"aa" is replaced by "a2". "bb" is replaced by "b2". "ccc" is replaced by "c3".


Example 2:

> Input:
> ["a"]
>
> Output:
> Return 1, and the first 1 characters of the input array should be: ["a"]

Explanation:
Nothing is replaced.


Example 3:

> Input:
> ["a","b","b","b","b","b","b","b","b","b","b","b","b"]
>
> Output:
> Return 4, and the first 4 characters of the input array should be: ["a","b","1","2"].

Explanation:
Since the character "a" does not repeat, it is not compressed. "bbbbbbbbbbbb" is replaced by "b12".
Notice each digit has it's own entry in the array.


Note:

+ All characters have an ASCII value in [35, 126].
+ 1 <= len(chars) <= 1000.

<a id="solution"></a>

### 解法

算法复杂度 `O(n)`，空间复杂度 `O(1)`

<a id="way"></a>

#### 思路

+ [Boyer and Moore majority voting algorithm](https://www.cs.utexas.edu/~moore/best-ideas/mjrty/)

第二题的思路相对直接会有一点绕。其仍然是 count 的想法，但是维护了两个计数器。

字符压缩题中也使用了类似的 count 思想，但是需要注意在循环之后还需要将最后一个可能的重复字符给补上。

<a id="code"></a>

#### 代码

```cpp
class Solution {
public:
    int majorityElement(vector<int>& nums) {
        int element = 0;
        int count = 0;
        for (int& num : nums) {
            if (count == 0) {
                count = 1;
                element = num;
            } else if (num == element) {
                ++count;
            } else {
                --count;
            }
        }
        return element;
    }
};
```

```cpp
class Solution {
public:
    vector<int> majorityElement(vector<int>& nums) {
        int cnt1 = 0;
        int cnt2 = 0;
        int val1, val2;
        for (int& num : nums) {
            if (cnt1 != 0 && val1 == num) {
                ++cnt1;
            } else if (cnt2 != 0 && val2 == num) {
                ++cnt2;
            } else if (cnt1 == 0) {
                cnt1 = 1;
                val1 = num;
            } else if (cnt2 == 0) {
                cnt2 = 1;
                val2 = num;
            } else {
                --cnt1;--cnt2;
            }
        }
        /* cout << "val1: " << val1 << " cnt1: " << cnt1 << endl; */
        /* cout << "val2: " << val2 << " cnt2: " << cnt2 << endl; */
        cnt1 = cnt2 = 0;
        for (int& num: nums) {
            if (num == val1) ++cnt1;
            else if (num == val2) ++ cnt2;
        }
        vector<int> result;
        int low = nums.size() / 3;
        if (cnt1 > low) result.push_back(val1);
        if (cnt2 > low) result.push_back(val2);
        return result;
    }
};
```

```cpp
class Solution {
private:
    void put_count(vector<char>& chars, int cur_count, int& cur_pos) {
        string s = to_string(cur_count);
        int length = s.size();
        for (char& c : s)
            chars[cur_pos++] = c;
    }
public:
    int compress(vector<char>& chars) {
        int length = chars.size();
        if (length == 0) return 0;
        int cur_pos = 0;
        char cur_char = ' ';
        int cur_count = -1;
        for (int j = 0; j < length; ++j) {
            if (cur_count == -1) {
                chars[cur_pos] = chars[j];
                cur_count = 1;
                cur_char = chars[j];
                /* position to store number */
                ++cur_pos;
            } else if (chars[j] == cur_char) {
                ++cur_count;
            } else {
                if (cur_count > 1)
                    put_count(chars, cur_count, cur_pos);
                cur_char = chars[j];
                chars[cur_pos] = chars[j];
                cur_count = 1;
                cur_pos++;
            }
        }
        if (cur_count > 1) {
            int n = 1;
            int m = cur_count;
            put_count(chars, cur_count, cur_pos);
        }
        return cur_pos;
    }
};
```

本文完
