---
layout: post
title: C++中动态内存分配
categories:
- programming
tags:
- operator new
---

在C++语言中，总共有5种内存分配区域：栈，堆（heap），自由存储区（free store），常量存储区，全局（静态）存储区。其中堆是用malloc/free一对系统库函数来管理动态内存的申请和释放，自由存储区是用new/delete一对操作符来动态管理内存的分配和释放。new/delete在标准中可以使用malloc/free实现，但是malloc/free不能使用new/delete实现。

他们之间的区别：

+ malloc/free是cstdlib中的函数，new/delete是操作符。
+ malloc/free只是分配所需的空间，若分配空间失败则返回空指针；new/delete不仅会分配空间，也会调用想用的构造函数和析构函数。其失败可以返回空指针，也可以抛出bad\_alloc的异常，或者调用相应的handler，其函数声明是void(\*)(void)，在new头文件中，通过set\_new\_handler来设置，其返回之前的处理，一般都是调用terminate()，结束程序的执行。

在C++中系统提供了几种全局的函数：

+ void \* operator new(size_t sz)
+ void \* operator new(size\_t sz, std::nothrow\_t&);
+ void \* operator new(size_t sz, void \*ptr);
+ void \* operator new(size_t sz,/\* args... \*/); // class specific

上面三个函数分别表示默认的new操作符，不抛出异常的new操作符，placement new操作符。

我们能重载的只能是在class specific的new构造函数，（上面给出new的版本，没有给出new[]，以及delete，delete[]版本）。

默认的delete版本：

+ void operator delete(void \*ptr);

在重载的时候，如果重载其中一个版本，则其它版本需要一同实现，以保证安全。

```cpp
#include <iostream>

using namespace std;

class A
{
public:
    static void* operator new(std::size_t sz)
    {
        std::cout<<"New"<<std::endl;
        return ::operator new(sz);
    }

    static void* operator new(std::size_t sz, const std::nothrow_t&)
    {
        std::cout<<"Nothrow:"<<std::endl;
        return ::operator new(sz);
    }

    static void operator delete(void *ptr)
    {
        std::cout<<"Delete"<<std::endl;
        ::operator delete(ptr);
    }

    static void operator delete(void *ptr, const std::nothrow_t &);

};

int main()
{
	// std::nothrow是提供的默认值
	// 调用不抛出异常的版本
    A *a = new(std::nothrow) A;
    delete a;

	a = new A; // 调用重载的版本
	delete a;

	void *ptr = ::operator new(sizeof(A));
	a = new(ptr) A; // placement new, 是系统默认的。
	a->~A(); // 需要主动调用析构函数，收回空间
	delete a;

    return 0;
}
```

上面是简易版本的重载。需要注意的是，重载时必须其函数是静态函数，函数的声明除了必须的函数参数，其它参数都是可选的。在重载的时候需要提供其它参数，就如上面代码中的std::nothrow。

1. <a href="http://en.cppreference.com/w/cpp/memory/new/operator_new" target="_blank"> Cpp Reference operator new</a>
2. <a href="http://en.cppreference.com/w/cpp/memory/new/operator_delete" target="_blank">Cpp Reference Operator delete </a>

本文完
