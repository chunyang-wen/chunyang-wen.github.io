---
layout: post
title: Compare in set and map
categories: [blog, stl]
tags: [cpp]
---

+ [简介](#intro)
+ [实现](#impl)

<a id="intro"></a>

### 简介

C++ STL 的 set 与 map 的模板参数中有一个是 `Compare` 类，该类的默认值是 `std::less<T>`。在某些场景下
我们需要自己定义这个 `Compare` 类。这个类返回的值要满足 `weak ordering`，即两个变量 a 和 b，满足下述关系
之一：`a<b`, `a>b`, `!(a<b) && !(a>b)`

> `a>b` 可以使用 `a<b` 来实现

<a id="impl"></a>

### 实现

我们想实现这么一个功能，判断两个字符是否相等，如果通过交换 i 和 j，当 `i%2 == j%2`，那仍然是相等的，
例如 `abc` 和 `cba`。

```cpp
#include<iostream>

#include<set>

#include<string>

using namespace std;

struct Cmp {
    bool operator()(const string& lhs, const string& rhs) const {
        if (lhs.size() != rhs.size()) {
            return lhs.compare(rhs) < -1;
        }
        // divide into two parts and compare
        string ll = "";
        string lr = "";
        string rl = "";
        string rr = "";
        int i = 0;
        int j = lhs.size();
        while (i < j) {
            ll += lhs[i];
            i += 2;
        }
        i = 1;
        while (i < j) {
            lr += lhs[i];
            i += 2;
        }
        i = 0; j = rhs.size();
        while (i < j) {
            rl += rhs[i];
            i += 2;
        }
        i = 1;
        while (i < j) {
            rr += rhs[i];
            i += 2;
        }
        sort(ll.begin(), ll.end());
        sort(lr.begin(), lr.end());
        sort(rl.begin(), rl.end());
        sort(rr.begin(), rr.end());
        auto status = ll.compare(rl) == 0 && lr.compare(rr) == 0;

        // return ll.compare(rl) < 0 || lr.compare(rr) < 0

        /* weak ordering */
        if (status == true) return false;
        return lhs.compare(rhs) < 0;
    }
};

int main(int argc, char* argv[]) {
    set<string, Cmp> s;
    cout << s.insert("abc").second << endl;
    cout << s.insert("cba").second << endl;
    return 0;
}
```

注意我们在判断排序后结果是否相等时，再次判断。因为如果我们只比较排序后的操作可能会导致重复插入元素。

本文完
