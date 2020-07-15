---
layout: post
title: Longest file path size
categories: [blog, algorithm]
tags: [dailycodingproblem, google]
---

+ toc
{:toc}

### Problem

This problem was asked by Google.

Suppose we represent our file system by a string in the following manner:

The string "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext" represents:

```bash

dir
    subdir1
    subdir2
        file.ext
```

The directory dir contains an empty sub-directory subdir1 and a sub-directory subdir2
containing a file file.ext.

The string
"dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"
represents:

```bash

dir
    subdir1
        file1.ext
        subsubdir1
    subdir2
        subsubdir2
            file2.ext
```

The directory dir contains two sub-directories subdir1 and subdir2. subdir1 contains a file
file1.ext and an empty second-level sub-directory subsubdir1. subdir2 contains a second-level
sub-directory subsubdir2 containing a file file2.ext.

We are interested in finding the longest (number of characters) absolute path to a file within
our file system. For example, in the second example above, the longest absolute path is
"dir/subdir2/subsubdir2/file2.ext", and its length is 32 (not including the double quotes).

Given a string representing the file system in the above format, return the length of the
longest absolute path to a file in the abstracted file system.
If there is no file in the system, return 0.

Note:

The name of a file contains at least a period and an extension.

The name of a directory or sub-directory will not contain a period.

### Solution

+ Each time we meet a file, calculate its path
  + A file is a name which contains a period
+ A new line is met, a new file or a new subdirectory
+ TAB means its indent

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
#include <stack>
#include <string>

using namespace std;

enum class Type {
    File = 0,
    Folder = 1,
};

struct Path {
    string name;
    Type type;
    int indent;
    int length;
    Path(Type t, int ind, int len, string n): type(t), indent(ind), length(len), name(n) {}
};

bool contains(const string& s, char c) {
    for (char ss: s) {
        if (c == ss) return true;
    }
    return false;
}

int parse(const string& s) {
    if (s.empty()) return 0;
    int max_size = 0;
    vector<Path> st;
    int i = 0;
    int indent = 0;
    int size = s.size();

    while (i < size) {
        int j = i;
        while (j < size && s[j] != '\n') ++j;
        string sub = s.substr(i, j - i);
        int prev_size = st.empty() ? 0 : st.back().length;
        cout << "name: " << sub << " size: " << sub.size() << " indent: " << indent << endl;
        if (contains(sub, '.')) {
            // a file
            cout << "Find a file: " << sub << endl;
            for (auto p : st) {
                cout << p.name << ":" << p.length << ", ";
            }
            cout << endl;
            max_size = max(max_size, prev_size + (int)sub.size());
        } else {
            // a subdirectory
            while (!st.empty() && st.back().indent >= indent) st.pop_back();
            int prev_size = st.empty() ? 0 : st.back().length;
            Path p(Type::Folder, indent, prev_size + sub.size() + 1, sub);
            cout << "add folder: " << p.length << endl;
            st.push_back(p);
        }

        ++j;
        indent = 0;
        while (j < size && s[j] == '\t') {
            ++j;
            ++indent;
        }
        i = j;
    }

    return max_size;
}

int main() {
    string str = "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext";
    cout << parse(str) << endl;
    string str1 = "dir";
    cout << parse(str1) << endl;
    string str2 = "dir\n\tdir2";
    cout << parse(str2) << endl;
    return 0;
}
```


