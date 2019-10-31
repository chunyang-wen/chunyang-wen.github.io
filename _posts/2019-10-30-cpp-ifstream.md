---
layout: post
title: std::ifstream in cpp
categories: [blog, cpp]
tags: [cpp]
---

* TOC
{:toc}

### Introduction

In this blog and next blog, we will introduce the functions in C++ that we read from and write
to files. It is the basic functionality when we learn programming.

### A simple example

```cpp
#include <array>
#include <fstream>
#include <iostream>
#include <string>

/* We assume there are 3 lines in test.txt
 * 1.3
 * 4
 * hello
 */

int main(int argc, char* argv[]) {

    std::string path = "test.txt";
    std::ifstream input(path, std::ios::in);
    double d1; input >> d1;
    input.get(); /* skip \n */
    char d2;
    char d3[2];
    input.get(d3, 2); // read count - 1 character */
    std::cout << "get(& char) d2: " << d3 << "\n";
    d2 = d3[0];
    input.putback(d2);
    input.get(d2);
    std::cout << "get(*ptr, count) d2: " << d2 << "\n";
    input.unget();
    input.read(reinterpret_cast<char*>(&d2), sizeof(d2));
    std::cout << "read(char*, count) d2: " << d2 << " gcount() = " << input.gcount() << "\n";


    input.get(); /* skip \n */
    std::array<char, 10> arr;
    input.getline(&arr[0], 10); /* default delimit: \n */
    std::cout << d1 << " " << d2 << " " << &arr[0] << std::endl;
    std::cout << std::boolalpha << "good = " << input.good() << " eof = " << input.eof() << std::endl;
    std::cout << "last: " << input.get() << std::endl;
    std::cout << std::boolalpha << "good = " << input.good() << " eof = " << input.eof() << std::endl;

    input.clear(); /* you should clear first, otherwise following code will fail */
    input.seekg(0, std::ios_base::seekdir::beg);
    std::cout << std::boolalpha << "good = " << input.good() << " eof = " << input.eof() << std::endl;
    std::string x;
    input >> d1 >> d2;
    input.get();
    std::getline(input, x);
    std::cout << "d1: " << d1 << " d2: " << d2 << " x: " << x << std::endl;
}
```

Compile and run:

```bash
g++ -std=c++11 program.cpp -o program
./program
```

### Common interfaces

#### Open & close

+ From constructor
+ `open(path)`
+ `close()`
+ `is_open()`

Open mode:

+ `std::ios::app`
+ `std::ios::ate`
+ `std::ios::trunc`
+ `std::ios::binary`
+ `std::ios::in`
+ `std::ios::out`

#### Status related

+ `good()`
+ `eof()`
+ `bad()`
+ `fail()`
+ `rdstate()`
+ `setstate()`
+ `clear()`

State(`iostate`):

+ `std::ios::goodbit`
+ `std::ios::badbit`
+ `std::ios::failbit`
+ `std::ios::eofbit`

#### Read data

+ `operator>>`
+ `get`
  + `get(char& c)`
  + `get(char* arr, count)`: read upto count - 1
  + `get(char* arr, count, delimit)`: read upto count - 1
+ `peek()`
+ `read(char*, size)`
+ `getline(char*, size, delimit)`: read upto size - 1
  + consume delimit
  + set an null at the next position of successful read.
+ `std::getline(stream, string, delimit)`

#### Position related

+ `seek`
  + `seekg(pos)`
  + `seekg(pos, refer)`
+ `tellg()`
+ `gcount()`

Direction:

+ `std::ios::seek_dir::beg`
+ `std::ios::seek_dir::cur`
+ `std::ios::seek_dir::end`

#### Un-read data

+ `putback(char c)`
+ `unget()`

### Tricks

Copy content of a file into a vector. **Each line should not contain spaces.**

> You can use to split words and convert them to upper case.

```cpp
#include <algorithm>
#include <fstream>
#include <iterator>
#include <iostream>
#include <string>
#include <vector>

int main(int argc, char* argv[]) {
    std::ifstream ifs("test.txt");
    std::vector<std::string> result;
    copy(std::istream_iterator<std::string>(ifs),
         std::istream_iterator<std::string>(),
         std::back_inserter(result));
    std::for_each(result.begin(), result.end(),
                  [](const std::string& s) { std::cout << s << std::endl; });
    auto x = [](std::string& str)->std::string {
        for (char& c : str) {
            c = ::toupper(c);
        }
        return str;
    };
    std::transform(begin(result), end(result), result.begin(), x);
    std::for_each(result.begin(), result.end(),
                  [](const std::string& s) { std::cout << s << std::endl; });
    return 0;
}
```

### References

+ <a href="https://en.cppreference.com/w/cpp/io/basic_ifstream" target="_blank">basic_ifstream</a>
