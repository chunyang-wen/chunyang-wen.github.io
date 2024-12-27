---
layout: post
title: Integer overflow
categories: [blog, leetcode]
tags: [leetcode]
---

In the world of data types, each type has its own range. Overflow can happen when you do math
on them. For example if you add one to the largest positive int32 number, you will get an overflow
error. But when the error happens, the behavior may be undefined. It can be rounded to the start
of the data or change to any invalid number.

+ toc
{:toc}


## Leetcode 228 Summary Ranges

The difficulty of the problem is easy. But I didn't make it at the first try.

```cpp
class Solution {
public:
    vector<string> summaryRanges(vector<int>& nums) {
        int size = nums.size();
        int i = 0;
        vector<string> result;
        while (i < size) {
            int n = i + 1;
            while (n < size && nums[n] - nums[n-1] == 1) ++n;
            string temp = to_string(nums[i]);
            if (n > i + 1) {
                temp += "->";
                temp += to_string(nums[n-1]);
            }
            result.push_back(temp);
            i = n;
        }
        return result;
    }
};
```

It failed with test case:

```bash
[-2147483648,-2147483647,2147483647]
```

I realized that it has the error.

```bash
Line 9: Char 40: runtime error: signed integer overflow: 2147483647 - -2147483647
cannot be represented in type 'value_type' (aka 'int') (solution.cpp)
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior prog_joined.cpp:18:40
```

I fixed it by adding the conversion to `long` to avoid the overflow.

```cpp
class Solution {
public:
    vector<string> summaryRanges(vector<int>& nums) {
        int size = nums.size();
        int i = 0;
        vector<string> result;
        while (i < size) {
            int n = i + 1;
            // A small trick to make sure all the number will be converted to long first
            while (n < size && (long)nums[n] - nums[n-1] == 1) ++n;
            string temp = to_string(nums[i]);
            if (n > i + 1) {
                temp += "->";
                temp += to_string(nums[n-1]);
            }
            result.push_back(temp);
            i = n;
        }
        return result;
    }
};
```

## Other two cases

### Binary search

It is a classic issue mentioned in a famous book *Programming pearls*.

```cpp
int bs(vector<int>& nums, int target) {
    int start = 0;
    int end = nums.size();
    while (start < end) {
        int mid = start + (end - start) / 2;
        //...
    }
}
```

The way we get the `mid` index is a bit tricky here. We can use:

```cpp
int mid = (start + end) / 2;
```

However, if there are two many elements in the `nums` array, you will get an overflow error.

### Size of a vector

```cpp
size_type size() const
```

The return value of a `size()` is unsigned type. You might get a large number if you do:

```cpp
#include <vector>
#include <iostream>

using namespace std;

int main() {
    vector<int> v;
    size_t value = v.size() - 1;
    // int value = v.size() - 1;
    cout << "Value: " << value << endl;
}
```

```bash
❯ g++ a.cpp
❯ ./a.out
Value: 18446744073709551615
```

Once we have an Out of Memory issue in a production component. It tries to allocate an insanely
large map data structure. The root cause is this kind of calculation which introduces overflow.

## Conclusion

We should be careful when applying computations. It is not always right to make the assumption
that everything is ideal and within the target range. To be more defensive will save your product
or company sometimes.

## References

- [Implicit type promotion rules](https://stackoverflow.com/questions/46073295/implicit-type-promotion-rules)
