---
layout: post
title: Generate random numbers in C++
categories: [blog, cpp]
tags: [cpp]
---

Some times we need a random number for sort or as the input
of our program. Previously we can use `rand()` to generate. Since c++ 11, we have a new
way to do so.

* TOC
{:toc}

### The old way

+ `RAND_MAX`: max number that `rand()` returns(included)
+ `rand()`: generates a number between [0, `RAND_MAX`]
  + If no `srand()` is called, it will generate number as `srand(1)` is called.
+ `srand(unsigned int)`: sets the seed
  + Usually we use `time(nullptr)` as the seed.

```cpp
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <random>

int main() {

    std::srand(std::time(nullptr));
    std::cout << rand() << std::endl;
    std::cout << RAND_MAX << std::endl;

    return 0;
}

```

### The new way

Random number can be generated using three steps:

+ initialize a random device
+ initialize a generator
+ initialize a distribution

```cpp
#include <algorithm>
#include <ctime>
#include <iostream>
#include <iterator>
#include <random>
#include <vector>

int main() {
    std::random_device rd;
    std::mt19937 generator(rd());
    std::uniform_int_distribution<> dis(1, 6);
    for (int i = 0; i < 10; ++i) {
        std::cout << dis(generator) << std::endl;
    }

    std::normal_distribution<> dis1(1, 6);
    for (int i = 0; i < 10; ++i) {
        std::cout << dis1(generator) << std::endl;
    }

    std::vector<int> vec{1,3,5};
    std::shuffle(std::begin(vec), std::end(vec), generator);
    std::copy(vec.begin(), vec.end(), std::ostream_iterator<int>(std::cout, ","));
    std::cout << "\n";


    return 0;
}
```

In <a href="https://en.cppreference.com/w/cpp/header/random" target="_blank">CppReference</a>,
it lists a bunch of predefined distributions.
