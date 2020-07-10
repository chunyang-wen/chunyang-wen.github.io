---
layout: post
title: C++ Exception
categories: [cpp]
tags: [cpp, exception]
---

+ [简介](#intro)
+ [异常声明](#declare-exception)
+ [异常捕获](#catch-exception)
+ [函数提供的保证](#guarantee)

<a id="intro"></a>

### 简介

C++ 中的异常主要分为两大类：

+ runtime\_error
  + 程序在运行时出现的异常
+ logic\_error
  + 程序本身的逻辑错误，例如函数入参不对

它们都派生自 `std::exception`.

+ 主要有构造函数（接受 `const std::string&` 和 `const char*`）
+ `what()` 函数返回当前异常的可描述信息

[Google code style](https://google.github.io/styleguide/cppguide.html#Exceptions) 是不建议使用的，
这个可能主要是因为他们很多代码都没有基于异常机制写。

<a id="declare-exception"></a>

### 异常声明

<a id="catch-exception"></a>

### 异常捕获

+ 如何捕获异常
+ 捕获异常时有哪些注意点

<a id="guarantee"></a>

### 函数提供的保证

+ 函数提供哪些保证
+ 出现异常时怎么处理：
  + 构造函数: 出现异常时，如果异常被捕获了，则所有已经构造好的成员对象会被析构，否则这个是实现
  相关的，即由实现来决定是否调用相关的析构函数，还是直接 `std::terminated`
  + 析构函数: 不允许出现异常，否则:`std::terminated`
+ 改变异常处理流程的函数
  + set\_unexpected
  + set\_terminated
  + set\_new\_handler


本文完

[1]:https://en.cppreference.com/w/cpp/language/exceptions
[2]:http://www.drdobbs.com/when-and-how-to-use-exceptions/184401836
[3]:https://en.cppreference.com/w/cpp/language/except_spec
[4]:https://en.cppreference.com/w/cpp/language/noexcept_spec
[5]:http://www.stroustrup.com/bs_faq2.html
