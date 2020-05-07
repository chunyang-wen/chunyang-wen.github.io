---
layout: post
title: Revisit compare in map and set
categories: [blog, stl]
tags: [cpp]
---

`map` and `set` are two common associative containers. By default, common data types
can be directly used as the key and their comparing method is `std::less`. On occassions,
we need to store user-defined type as the key. We need to define the comparing method for
the type.

+ toc
{:toc}

### Main course

There are two ways that we can set the comparing functions.

+ A struct class which defines `operator()`
+ A lambda function

```cpp
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <functional>

using namespace std;
class Solution {

    struct Cmp {

        bool operator()(const string& l, const string& r) const {
            string ll = l;
            string rr = r;
            sort(begin(ll), end(ll));
            sort(begin(rr), end(rr));
            cout << "ll: " << ll <<endl;
            cout << "rr: " << rr << endl;
            return ll.compare(rr) < 0;
        }
    };
public:
    vector<vector<string>> groupAnagrams(vector<string>& strs) {
        const function<bool(const string&, const string&)> cmp = [](const string& l, const string& r) {
            string ll = l;
            string rr = r;
            sort(begin(ll), end(ll));
            sort(begin(rr), end(rr));
            cout << "ll: " << ll <<endl;
            cout << "rr: " << rr << endl;
            return ll.compare(rr) < 0;
        };
        /* Method 1: */
        map<string, vector<string>, decltype(cmp)> m(cmp);

        /* Method 2: */
        map<string, vector<string>, Cmp> m1;
        vector<vector<string>> result;
        for (string& s: strs) {
            m[s].push_back(s);
        }
        for (auto& x : m) {
            result.push_back(x.second);
        }
        return result;
    }
};


int main() {

    vector<string> s{"hi", "ih"};
    Solution sol;
    sol.groupAnagrams(s);

    return 0;
}
```

+ If we choose to use a struct type, `operator()` must be decorated by `const` (not the argument)
  + Otherwise you will get a compiliation error
+ If we we choose to use a lambda function, we have to pass the function to the constructor
  + Otherwise you will get a wierd error: `bad_function_call`

### Related

+ [Compare in set and map](/blog/stl/cpp-set-compare.html)
