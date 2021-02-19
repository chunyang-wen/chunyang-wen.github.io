---
layout: post
title: Pick a number randomly from an unlimited stream
categories: [blog, algorithm]
tags: [dailycodingproblem, facebook]
hidden: true
---

+ toc
{:toc}

### Problem

This problem was asked by Facebook.

Given a stream of elements too large to store in memory, pick a random element from
the stream with uniform probability.

### Solution

This problem can be extended to pick k number randomly with equal probability.

+ Pick one number
+ Pick K number

```cpp
#include <algorithm>
#include <iostream>
#include <iterator>
#include <vector>
#include <cstdlib>

using namespace std;

template<class Type>
class Generator {
public:
    typedef Type DataType;
    virtual bool HasNext() = 0;
    virtual Type Next() = 0;
    virtual void Reset() = 0;
};

class IntegerGenerator: public Generator<int> {
public:
    IntegerGenerator(int n, const int limit): i(0), _v(n) {
        generate(begin(_v), end(_v), [&]() {
            return rand() % limit;
        });
        copy(begin(_v), end(_v), ostream_iterator<int>(cout, ","));
        cout << "\n";
    }

    bool HasNext() {
        return i < _v.size();
    }

    int Next() {
        return _v[i++];
    }

    void Reset() { i = 0; }

private:
    vector<Generator<int>::DataType> _v;
    int i;
};

template<class Type>
int pick_one_number(Generator<Type>& g) {
    int result = 0;
    int cur = 1;
    while (g.HasNext()) {
        auto r = rand();
        auto p = r % cur;
        auto next = g.Next();
        cout << "R: " << r << " cur: " << cur << " Prob: " << p << " next: " << next << "\n";
        if (p < 1) {
            result = next;
        }
        ++cur;
    }
    return result;
}

template<class Type>
vector<int> pick_k_number(Generator<Type>& g, int k) {
    vector<int> result;
    int cur = 1;
    while (g.HasNext()) {
        auto next = g.Next();
        if (result.size() < k) {
            result.push_back(next);
        } else {
            auto r = rand() % cur;
            cout << "Whether select: " << r << "/" << cur << "\n";
            if (r < k) {
                auto kk = rand() % k;
                cout << "Select element: " << kk << "\n";
                result[kk] = next;
            }
        }
        ++cur;
    }
    return result;
}

int main() {
    srand(time(nullptr));
    IntegerGenerator gen(100, 1000);
    auto n = pick_one_number(gen);
    cout << "Picked number = " << n<< endl;
    gen.Reset();
    auto r = pick_k_number(gen, 20);
    cout << "Select K = ";
    copy(begin(r), end(r), ostream_iterator<int>(cout, ","));
    cout << "\n";

    return EXIT_SUCCESS;
}

```

### Comments

+ Reservoir Sampling
