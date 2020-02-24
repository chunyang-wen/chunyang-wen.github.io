---
layout: post
title: std::ofstream in cpp
categories: [blog, cpp]
tags: [cpp]
---

* TOC
{:toc}

### Introduction

Cpp's `std::ofstream` is very similar to its `std::ifstream`.


### A simple example

```cpp
#include <fstream>
#include <iostream>

int main(int argc, char* argv[]) {

    std::ofstream ofs("out.txt");
    int a = 3;
    double b = 4;
    ofs << a << "\n" << b << "\n";
    int d = 4;
    ofs.write(reinterpret_cast<char*>(&d), sizeof(d));
    char c = '\n';
    ofs.write(&c, sizeof(char));
    ofs.put('X');
    ofs.flush();
    ofs.close();

    std::ifstream ifs("out.txt");
    int e; double f;
    ifs >> e >> f;
    ifs.get(); // skip '\n'
    int g;
    ifs.read(reinterpret_cast<char*>(&g), sizeof(g));
    std::cout << e << " " << f << " " << e << std::endl;
    std::cout << std::boolalpha << ifs.eof() << std::endl;
    ifs.close();

    return 0;
}
```

### Common interfaces

### Open & close

similar to `ifstream`.

#### Write data

+ `operator<<`
+ `put`
+ `write(char*, count)`

#### Position

+ `tellp()`
+ `seekp(pos, refer)`

### Control output formats

Sometimes we want to control the output. Cpp has provided lots of functions and `fmtflags`
to help users.

#### number related

+ `std::boolalpha`
+ `std::hex`, `std::oct`, `std::dec`
+ `std::scientific`
+ `std::fixed`
+ `std::showbase`
+ `std::showpos`
+ `std::showpoint`
+ `setf`, `unsetf`
+ `flags`

#### Length and alignment

+ `setwitdh`, `width`
+ `setprecision`, `precision`
+ `setfill`, `fill`


#### A complete example

```cpp
#include <algorithm>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <vector>


int main(int argc, char* argv[]) {

    std::ofstream ofs("out.txt");
    std::ios::fmtflags flags = ofs.flags();
    int a = 3;
    ofs << std::setw(8) << std::setfill('-') << std::left << std::showbase << std::hex << a << "\n";

    ofs.width(4);
    ofs.fill('+');
    ofs.setf(std::ios::right|std::ios::showbase);
    ofs << a << "\n";

    double c = 3.4;
    ofs << std::showpos << std::showpoint << c << "\n";

    double e = 3.141592653;
    ofs.unsetf(std::ios::showpos);
    ofs << std::setprecision(3) << e << "\n";

    // reset flags
    ofs.flags(flags);
    double d = 3.4;
    ofs << d << "\n";

    ofs.flush();
    ofs.close();

    return 0;
}
```

### Tricks

```cpp
#include <algorithm>
#include <fstream>
#include <iterator>
#include <string>
#include <vector>

int main(int argc, char* argv[]) {

    std::ofstream ofs("out.txt");
    std::vector<std::string> result {"Hello", "The", "World"};
    std::copy(result.begin(), result.end(), std::ostream_iterator<std::string>(ofs, "\n"));
    std::vector<int> result1 {1, 3, 5};
    std::copy(result1.begin(), result1.end(), std::ostream_iterator<int>(ofs, "\n"));

    return 0;
}
```

### References

+ <a href="https://en.cppreference.com/w/cpp/io/basic_ofstream" target="_blank">ofstream</a>

