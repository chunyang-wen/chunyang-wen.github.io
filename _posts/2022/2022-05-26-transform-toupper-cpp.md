---
layout: post
title: std::transform not working with std::toupper
categories: [blog, cpp]
tags: [cpp]
---

`ctype` 中定义了一些比较实用的函数，例如 `toupper`, `tolower`, `isalpha` 等等。在 C++
中如何实用这些函数呢？实用 `cctype`，然后就可以在 `std` 的命名空间中使用这些函数。

+ toc
{:toc}

## 背景

一个字符串的大小写转换程序如下：

```cpp
#include <cctype>
#include <vector>

int main(int argc, char* argv[]) {

    std::vector<char> chars{'a', 'b', 'c'};
    int size = chars.size();
    for (int i = 0; i < size; ++i) {
        chars[i] = std::toupper(chars[i]);
    }

}
```

## 问题

洋洋洒洒写了那么多其实就是将数组中的字符进行大小写转换，其实 `transform`
就可以完成这个功能。

```cpp
#include <algorithm>
#include <cctype>
#include <vector>

int main(int argc, char* argv[]) {

    std::vector<char> chars{'a', 'b', 'c'};
    std::transform(begin(chars), end(chars), begin(chars), std::toupper);
}
```

但是这个程序实际上没有办法编译，出错信息如下：

```cpp
error: no matching function for call to 'transform'
    std::transform(begin(v), end(v), begin(v), std::toupper);
    ^~~~~~~~~~~~~~
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/algorithm:1979:1: note: candidate template ignored: couldn't infer template argument '_UnaryOperation'
transform(_InputIterator __first, _InputIterator __last, _OutputIterator __result, _UnaryOperation __op)
^
/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk/usr/include/c++/v1/algorithm:1989:1: note: candidate function template not viable: requires 5 arguments, but 4 were provided
transform(_InputIterator1 __first1, _InputIterator1 __last1, _InputIterator2 __first2,
^
1 error generated.
```

大概意思是没有找到合适的 `transform` 函数。

## 解决方案

```cpp
#include <algorithm>
#include <cctype>
#include <iostream>
#include <vector>

int main(int argc, char* argv[]) {
    std::vector<char> v{'a', 'b', 'c'};
    std::cout << std::toupper('v') << std::endl;
    std::cout << ::toupper('v') << std::endl;
    std::transform(begin(v), end(v), begin(v), ::toupper);
    std::transform(begin(v), end(v), begin(v), [](char c) {return std::toupper(c);});
    std::transform(begin(v), end(v), begin(v), (int(*)(int))(std::toupper));
    //std::transform(begin(v), end(v), begin(v), std::toupper);
}
```

## 刨根问题

为什么会出现这种情况呢？怀疑的原因如下：

+ `toupper` 定义冲突
+ `ADL`: [Argument Dependent Lookup](https://en.wikipedia.org/wiki/Argument-dependent_name_lookup)

### `toupper` 定义冲突

即在 `std` 的命名空间中，存在 2 处及以上的定义。但是按照经验，应该要报一个类似于 `* ambiguous *`。
去 [Cpp Reference](en.cppreference.com/)

![toupper](/images/cpp/toupper.png)

的确是有 2 处定义。在 `cctype` 中的只是做了一层简单的引入。

```cpp
#include <ctype.h>
namspace std {
    using ::toupper;
}
```

在 `<locale>` 中定义的 `toupper` 会另外一个参数 `locale`。的确是二者使用冲突。

### Argument Dependent Loop or Koenig lookup

+ [GotW](http://www.gotw.ca/gotw/030.htm)
+ [Wikipedia](https://en.wikipedia.org/wiki/Argument-dependent_name_lookup)

主要是针对 `unqualified function`。在查找是会同时查找它参数所在的命名空间。但是我的调用都已经加
`std` 的修饰。

## 总结

后来在 stackoverflow 上找到一个 [帖子](https://stackoverflow.com/a/7132065/2567512)。根本原因还是
编译器找错了函数。但是报错信息显然有问题。
