---
layout: post
title: An autocomplete system
categories: [blog, algorithm]
tags: [dailycodingproblem]
---

+ toc
{:toc}

### Problem

This problem was asked by Twitter.

Implement an autocomplete system. That is, given a query string s and a set of all
possible query strings, return all strings in the set that have s as a prefix.

For example, given the query string de and the set of strings [dog, deer, deal], return [deer, deal].

Hint: Try preprocessing the dictionary into a more efficient data structure to speed up queries.

### Solution

+ Use a Trie data structure

```cpp

#include <algorithm>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
#include <iterator>

struct TrieNode {
    bool is_end;
    std::vector<TrieNode*> next;
    TrieNode():is_end(false), next(26) {}
};


class AutocompleteSystem {
public:
    void add(const std::string& str);
    std::vector<std::string> get_suggestion(const std::string& input);
private:
    TrieNode _trie;
};

void AutocompleteSystem::add(const std::string& str) {
    TrieNode* node = &_trie;
    for (char c : str) {
        auto index = c - 'a';
        if (node->next[index] == nullptr) {
            node->next[index] = new TrieNode;
        }
        node = node->next[index];
    }
    node->is_end = true;
}

std::vector<std::string> AutocompleteSystem::get_suggestion(
        const std::string& input) {
    TrieNode* node = &_trie;
    for (char c: input) {
        auto index = c - 'a';
        if (node->next[index] == nullptr) return {};
        node = node->next[index];
    }
    std::vector<std::string> result;
    std::function<void(const TrieNode*, std::string&)> search = [&](
        const TrieNode* node, std::string& cur) {
        if (node->is_end) {
            result.push_back(cur);
        }
        int i = 0;
        for(auto n: node->next) {
            if (n != nullptr) {
                cur.push_back(i + 'a');
                search(n, cur);
                cur.pop_back();
            }
            ++i;
        }
    };
    std::string start = input;
    std::cout << "start from: " << input << std::endl;
    search(node, start);
    return result;
}

int main() {
    AutocompleteSystem system;
    system.add("dog");
    system.add("deer");
    system.add("deal");
    auto res = system.get_suggestion("de");
    std::copy(begin(res), end(res), std::ostream_iterator<std::string>(std::cout, ","));
    res = system.get_suggestion("d");
    std::copy(begin(res), end(res), std::ostream_iterator<std::string>(std::cout, ","));
    res = system.get_suggestion("o");
    std::copy(begin(res), end(res), std::ostream_iterator<std::string>(std::cout, ","));
}
```

### Comments

This is a very naive implementation of Trie. It does not take following into consideration:

+ case
+ characters besides lower case letter
+ memory efficiency
