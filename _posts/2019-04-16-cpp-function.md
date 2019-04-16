---
layout: post
title: C++ bind and function
categories: [cpp]
tags: [bind, function]
---

+ [简介](#intro)
+ [bind 函数](#bind)
+ [常用函数和例子](#function-example)

<a id="intro"></a>

### 简介

C++ 后面的版本中提供很多函数对象，可以很方便的使用，例如 `less`, `greater` 等。当函数对象有多个参数
时，我们可以通过 `bind` 来绑定部分参数，使得函数对象的使用范围更大。例如我想替换数组中所有大于 3 的
元素为 0.

```cpp
std::vector<int> a {1, 5, 9};
auto f = std::bind(std::greater<int>(), _1, 3);
std::replace_if(a.begin(), a.end(), f, 0);
std::copy(a.begin(), a.end(), std::ostream_iterator<int>(cout, "\n"));
```

利用 STL 提供的算法，将数组的满足指定条件的元素都替换为新的元素。

<a id="bind"></a>

### bind 函数

`bind` 是 C++ 提供的函数，它可以给一个：

+ 函数指针
+ 函数对象
+ 成员函数
+ 成员变量

绑定对应的元素，对于每一个位置的元素有 3 中输入：

+ `std::placehoders`: `_1`, `_2` 等
+ `std::cref`，`std::ref`: 绑定了相关的引用
+ 其它值：会调用其复制构造函数，除非使用上面的 `ref` 和 `cref` 来绑定

#### 函数指针

```cpp
void sum_3(int a, int& b, const int& c) {
    cout << a << " " << b << " " << c << endl;
    cout << a + b + c << endl;
}

int main(int argc, char* argv[]) {
    using namespace placeholders;
    int a = 3;
    int b = 4;
    auto f = std::bind(sum_3, _1, std::ref(a), std::cref(b));
    f(1);
    return 0;
}
```

在实际代码验证中：

+ 如果不是以引用的形式传递参数不会报错
+ 在调用 `f` 时，额外的参数会被忽略不会报错

#### 函数对象

函数对象就是类似 `std::less` 的对象，或者是实现 `operator()` 的对象。

```cpp

struct Greater {
    bool operator()(const int& lhs, const int& rhs) {
        return lhs >= rhs;
    }
};

int main(int argc, char* argv[]) {
    using namespace placeholders;
    vector<int> a{1,3,5,6};
    auto f = bind(greater_equal<int>(), _1, 6);
    auto e1 = remove_if(a.begin(), a.end(), f);
    copy(a.begin(), e1, ostream_iterator<int>(cout, ","));
    cout << "\n";
    auto g = bind(Greater(), _1, 3);
    auto e2 = remove_if(a.begin(), a.end(), g);
    copy(a.begin(), e2, ostream_iterator<int>(cout, ","));
    cout << "\n";
    return 0;
}
```

#### 成员函数和成员变量

当绑定非静态成员函数或者成员变量时，`bind` 调用后的第一个参数必须是对象的引用或者指针。

```cpp

struct Hello {
    void print(int a, int b) {
        cout << a << " " << b << endl;
    }
    int a;
};

int main(int argc, char* argv[]) {
    using namespace placeholders;

    Hello h;

    auto f = bind(&Hello::print, h, _1, 3);
    f(4);

    auto g = bind(&Hello::a, _1);
    cout << g(&h) << endl;
    g(h) = 6;
    cout << g(h) << endl;

    return 0;
}
```

指向成员变量时，实际上就是获得了一个指针。

指向成员函数时还可以使用 `mem_fn` 来实现，但是尽量使用 `bind`，这些接口可能在后续被废弃掉。从使用上
来看，它不需要知道成员函数有几个参数。

```cpp
auto f = mem_fn(&Hello::print);
f(h, 1, 2);
```

<a id="function-example"></a>

### 常用函数和例子

#### 四则运算

+ `plus`
+ `minus`
+ `multiplies`
+ `divides`
+ `modulus`
+ `negate`

#### 比较操作

+ `equal_to`
+ `not_equal_to`
+ `greater`
+ `greater_than`
+ `less`
+ `less_than`

#### 逻辑操作

+ `logical_and`
+ `logical_or`
+ `logical_not`

#### 位操作

+ `bit_and`
+ `bit_or`
+ `bit_xor`
+ `bit_not`

还提供很多类型的 `hash` 函数，包括 `char`， `int`, `long`, `float`，`double`，以及各种指针。

本文完
