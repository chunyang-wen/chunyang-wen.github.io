---
layout: post
title: Combinations of words
categories: [blog, algorithm]
tags: [dailycodingproblem, microsoft]
---

+ toc
{:toc}

### Problem

This problem was asked by Microsoft.

Given a dictionary of words and a string made up of those words (no spaces),
return the original sentence in a list. If there is more than one possible reconstruction,
return any of them. If there is no possible reconstruction, then return null.

For example, given the set of words 'quick', 'brown', 'the', 'fox', and the
string "thequickbrownfox", you should return ['the', 'quick', 'brown', 'fox'].

Given the set of words 'bed', 'bath', 'bedbath', 'and', 'beyond', and the string
"bedbathandbeyond", return either ['bed', 'bath', 'and', 'beyond] or ['bedbath', 'and', 'beyond'].

### Solution

+ Iterate through the dict, minimize combinations we need to try
+ Return as soon as we find a valid combination

```cpp
#include <algorithm>
#include<iostream>
#include <string>
#include <vector>
#include <set>
#include <functional>

using namespace std;

vector<string> combinations_of_words(const set<string>& dict, const string& str) {
    vector<string> result;

    int min_len = INT_MAX, max_len = INT_MIN;
    for_each(begin(dict), end(dict), [&](const string& s) {
        min_len = min(min_len, static_cast<int>(s.size()));
        max_len = max(max_len, static_cast<int>(s.size()));
    });

    cout << "min_len: " << min_len << " max_len: " << max_len << endl;

    function<bool(int)> split = [&](int start) {

        if (start >= str.size()) return true;

        int limit = min(start + max_len, static_cast<int>(str.size()));
        cout << "limit: " << limit << endl;
        for (int i = start + min_len; i <= limit; ++i) {
            string cur = str.substr(start, i - start);
            cout << "i: " << i << " cur: " << cur << endl;
            if (dict.find(cur) == dict.end()) {
                cout << "bad: " << cur << endl;
                continue;
            }
            result.push_back(cur);
            if (split(i)) {
                return true;
            }
            result.pop_back();
        }
        return false;
    };

    split(0);

    return result;
}

int main() {

    set<string> dict {"quick", "brown", "the", "fox"};
    auto x = combinations_of_words(dict, "thequickbrownfox");
    copy(begin(x), end(x), ostream_iterator<string>(cout, ","));
    cout << endl;

    set<string> dict1 {"bedd", "bath", "bedbath", "and", "beyond"};
    auto xx = combinations_of_words(dict1, "bedbathandbeyond");
    copy(begin(xx), end(xx), ostream_iterator<string>(cout, ","));
    cout << endl;


    return 0;
}
```
