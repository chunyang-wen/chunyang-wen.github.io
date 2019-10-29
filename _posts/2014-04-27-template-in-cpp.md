---
layout: post
title: C++中模板的学习
categories: [blog, cpp]
tags: [cpp]
redirect_from:
 - /programming/template-in-cpp
---


C++中的模板是C++中实现元编程的一种主要途径。元编程，即编写程序的程序。维基百科上说：
>Metaprogramming is the writing of computer programs that write or manipulate other programs (or themselves) as their data, or that do part of the work at compile time that would otherwise be done at runtime. In some cases, this allows programmers to minimize the number of lines of code to express a solution (hence reducing development time), or it gives programs greater flexibility to efficiently handle new situations without recompilation.

维基百科上说是在编译器间完成，其实脚本像Ruby可以在运行期间可变程序的行为。首先来看看tempalte的一些基本应用。

+ 函数模板

```cpp
template<typename T1, typename T2>
std::common_type<T1,T2>::type add(T1 t1, T2 t2);
```

上述是声明一个函数模板，其可以针对两种类型相加，然后给出结果。common_type是c++11中在type_traits中引入的。如果T1和T2没有公共类型就会出错。

+ 类模板

```cpp
template<typename T>
class Stack
{
private:
	T value;
	//...other stuff...
};
```

上述是声明一个简单的Stack类，其中模板参数表示其可以存储任何类型。

一般主要就是用于以上两个目的：函数模板和类模板。函数模板和类模板是不一样的，类模板有特化，偏特化和完全特化；函数模板**没有**，函数模板只有重载。看看下面一个例子：

```cpp
// 1
template<typename T>
void f(T);

// 2
template<>
void f<int*>(int*);

// 3
template<typename T>
void f(T*);

int a;
int *b = &a;
f(b)
```

上述的f函数调用哪一个函数呢？绝大多数人凭着自己直觉会觉得肯定调用2，因为这个是最特殊的。但是其实不是，它调用第三个。（为了能够调用，大家可以给他们分别加上函数体，打印相关东西）

函数调用的顺序如下：

+ plain old function: 没有模板修饰的，匹配的优先级最高。
+ primary template overload: 稍微特化一点的模板。
+ primary template: 最开始的模板。

上述函数调用使用的是primary template overload这种调用方式。第一个模板实际上是T-\>T的形式，而第三个模板是T-\>T\*的形式。上面是函数模板与类模板一个重要的区别，需要仔细体会。

函数模板的功能很大，看看如何来发挥一下它。首先打印一个10！，在编译期间完成计算。

```cpp
template<int n>
struct Factor
{
	const static int Value = Factor<n-1>::Value * n;
};

template<>
struct Factor<1>
{
	const static int Value = 1;
};

cout<<Factor<10>::Value<<endl;
```

当然这种方式必须给n一个定值，否则就会编译出错。在C++11中还引入可变模板参数。

```cpp
template<typename T, typename...Args>
void print(T t, Args...args)
{
	cout<<t<<endl;
	print(args...);
}
```

上述是可变模板参数编写的print函数，我们可以给print传入类型的值。

模板还可以为我们带来一些比较奇怪的好处：帮助我们访问类的私有变量。

```cpp
class Earth
{
private:
	int private_;
public:
	template<typename T>
	void f(T t);
	void g();
};
```

上面是一个类的定义，我们可以通过哪些方式访问其私有变量private\_呢？

+ 给此类添加一个公有函数
+ 利用内存布局的知识，将其重新解释reinterpret\_cast<int*>(&earth\_obj)
+ 添加友元函数
+ 给类增加一个模板函数：Bingo.

```cpp
struct Y{};
template<>
void Earth::f<Y>(Y y) {/* hacker's laugh */};
```

接下来研究一下《More Exceptional C++》（Herb sutter）上的一个例子。

```cpp
template<typename T1, typename T2>
void g(T1, T2);
template<typename T> void g(T);
template<typename T> void g(T,T);
template<typename T> void g(T*);
template<typename T> void g(T*,T);
template<typename T> void g(T, T*);
template<typename T> void g(int, T*);
template<> void g<int>(int);
void g(int, double);
void g(int);

int i;
double d;
float f;
complex<double> c;

// test cases
g(i);         // 1
g<int>(i);    // 2
g(i,i);       // 3
g(c);         // 4
g(i,f);       // 5
g(i,d);       // 6
g(c, &c);     // 7
g(i, &d);     // 8
g(&d, d);     // 9
g(&d);        // 10
g(d, *i);     // 11
g(&i,&i);     // 12
```

上面提到函数模板只有重载，而没有偏特化这种形式，再强调一次，在匹配时，

+ 自由函数，函数参数类型必须完全一致，不允许转换
+ 函数模板-\>最特化的模板
+ 函数模板-\>通用模板

匹配结果如下：

+ 第一个函数匹配：g(int);
+ 第二个匹配：template<\> void g<int\>(int);
+ 第三个匹配：template<typename T\> void g(T,T);
+ 第四个匹配：template<typename T\> void g(T);
+ 第五个匹配：template<typenmae T1, typename T2\> void g(T1, T2);
+ 第六个匹配：void g(int, double);
+ 第七个匹配：template<typename T\> void g(T, T*);
+ 第八个匹配：template<typename T\> void g(int, T*);
+ 第九个匹配：template<typename T\> void g(T*,T);
+ 第十个匹配：template<typename T\> void g(T*);
+ 第十一个匹配：template<typename T1, typename T2\> void g(T1, T2);
+ 第十二个匹配：template<typename T\> void g(T,T);

总结一下：C++中的模板帮助我们编写通用的函数和类，而且也提供了元编程的能力。但是每一技术都需要仔细去研究才会得心应手。

本文完
