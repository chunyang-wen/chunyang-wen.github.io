---
layout: post
title: Implicit conversions
categories: [blog, translating]
tags: [cpp]
redirect_from:
 - /translating/implicit-conversions
---


该博文翻译自[Implicit conversion](http://en.cppreference.com/w/cpp/language/implicit_cast)


## 目录


[转换优先级](#Convert_order)
[左值转换](#lvalue_convert)
&nbsp;&nbsp;&nbsp;&nbsp;[左值到右值转换](#lvalue_rvalue)
&nbsp;&nbsp;&nbsp;&nbsp;[数组名到指针的转换](#array_name_pointer)
&nbsp;&nbsp;&nbsp;&nbsp;[函数指针的转换](#function_ptr)
[数值提升](#integer_promotion)
&nbsp;&nbsp;&nbsp;&nbsp;[整型提升](#integral_promotion)
[数值转换](numeric_conversion)
&nbsp;&nbsp;&nbsp;&nbsp;[整型转换](#integral_conversion)
&nbsp;&nbsp;&nbsp;&nbsp;[浮点转换](#float_conversion)
&nbsp;&nbsp;&nbsp;&nbsp;[浮点-整型转换](#float_integer)
&nbsp;&nbsp;&nbsp;&nbsp;[指针转换](#ptr_conversion)
&nbsp;&nbsp;&nbsp;&nbsp;[指向成员指针转换](#ptr_mem_conversion)
[布尔转换](#bool_conversion)
[修饰符转换](#cv_conversion)
[安全bool值问题](#safe_bool)



隐式转换发生在将任何表达式需要类型T1应用在某上下文不接受该类型，但是接受其他某类型T2的场景中，特别的是：

+ 类型T1表达式应用于接受类型为T2的函数参数的函数调用中
+ 类型T1是某个希望得到类型为T2的操作符上
+ 初始化类型为T2的变量，包括函数返回值
+ 类型为T1的表达式应用于switch语句中（T2是整形变量）
+ 表达式应用于if语句中（T2是bool型变量）

在以上场景中，当仅存在一个从T1到T2的隐式转换时，程序可以正常编译。如果存在多个函数或者运算符重载函数被调用，当从T1到T2的每一个可能的隐式转换发生后，重载决议才会执行。


<a id="Convert_order"></a>
## 转换的优先级
---

隐式转换的序列的优先级如下：

+ 0或者1个标准转换序列
+ 0或者1个用户定义的转换
+ 0或者1个标准转换序列

当考虑构造函数或者用户自定义的转换函数时，只有标准的转换序列是允许的（否则，用户自定义的转换会形成转换链）。当从语言的内置类型之间转换时，只有标准转换序列是允许的。

一个标准的转换序列由如下组成，其优先级如下：

+ 0或者1个左值转换
+ 0或者1个数值提升或者数值转换
+ 0或者1个资格调整（Qualification Adjustment）

用户定义的转换由如下组成：

+ 0或者1个non-explicit single-argument构造函数或者non-explicit转换函数调用

一个表达式e可以隐式转换为T2，当且仅当T2是从e复制初始化(copy-initialization)，即T2 t = e。注意这和直接构造初始化不一样 T2 t(e)，此时需要额外考虑显式的构造函数和转换函数。

上述规则的一个例外是如下五个上下文中特殊的隐式转换，此时需要bool类型的变量：

+ if, while, for中的控制语句
+ 逻辑运算符，！，&&， ||
+ 条件运算符: ?:
+ static\_assert
+ noexcept

在上述上下文环境中隐式转换按如下方式进行 bool t(e)。用户显式定义的转换函数：T::operator bool()const将会被考虑。这些表达式contextually convertible可转换为bool。

在如下上下文中，需要上下文相关的类型T，只有当类类型E仅有一个用户定义的转换函数时，且其返回值是cv T或者是cv T的引用。

+ 新表达式中的数组界限（T is std::size\_t）
+ 数组界限的声明（T is std::size\_t）
+ 删除运算符中的参数（T is any object pointer type）（since c++14）
+ 整形常量，使用字面类型（T is any integral or unscoped enumeration type and the selected user-defined conversion function is constexpr）

表达式e是contextually implicit转换成T。

<a id="lvalue_convert"></a>
## 左值转换
---


左值转换是指在需要右值的上下文中提供左值。

<a id="lvalue_rvalue"></a>
### 左值到右值的转换
---


任何非函数，非数组的类型T的glvalue可以被隐式转换成相同类型的prvalue。如果T是非类类型，这种转换会移除cv修饰。除非遇到不估值的上下文，例如sizeof,typeid, noexcept, decltype，这种转换会使用原来的glvalue为构造函数的参数，复制构造类型为T的临时变量，临时变量会以prvalue形式返回。如果glvaule是nullptr\_t，返回的变量值为nullptr。


<a id="array_name_pointer"></a>
### 数组名到指针的转换
---


类型是长度为N，类型T数组的左值或者右值，或者是未知长度类型T的数组可以隐式转换为指向T的prvalue。产生的指针指向数组的第一个元素。

<a id="function_ptr"></a>
### 函数到指针的转换
---


函数类型T的左值可以隐式转换为一个指向该函数的prvalue。这个不适用于non-static成员函数，因为指向非静态成员函数的左值不存在。

<a id="integer_promotion"></a>
## 数值提升
---

<a id="integral_promotion"></a>
### 整型提升
---


小整型的prvalue值（例如char）会转换成表示范围个更大的整型（例如int）。特别是在算数操作符不接受类型比int小的数作为参数，整型提升自动执行。这种转换保持之前的值。

下面是一些整型提升的场景：

+ signed char或者signed short转换成int
+ unsigned char或者unsigned short转换成int。如果int可以表示unsigned int，unsigned int也转换为int。
+ char可以转变成int或者unsigned int，取决于底层的是signed char还是unsigned char
+ wchar\_t, char16\_t和char32\_t可转变成下列类型（保证可以容纳下所有的值）：int, unsigned int, long, unsigned long, long long, unsigned long long。
+ unscoped enumeration类型，如果它的潜在类型没有规定，那么它会按以下列表转换（保证可以容纳其所有的值）：int, unsigned int, long, unsigned long, long long, unsigned long long。如果值的范围太大，那么没有整型提升。
+ 位域类型：如果int可以表示其所有范围的值，则转换成int；否则转换成unsigned int；其它情况没有整型提升。

>枚举类型如果底层实现类型指定了，其整型提升按照指定的类型提升规则进行提升。

<a id="float_promotion"></a>
### 浮点提升
---


float类型转换成double，其值不变。

<a id="numeric_conversion"></a>
## 数值转换
---

与提升不同，数值转换可能会改变值，造成精度的丢失。


<a id="integral_conversion"></a>
### 整型转换
---


整型和unscoped枚举类型可以转换成任何其它的整型值。如果转换是按如下方式进行，那么是整型提升，不是整型转换。

+ 如果目标类型是unsigned，结果的类型是使用模(2^n)的得到的最小无符号数值。其中n是目标类型的长度。依据目标类型是宽或者窄，有符号整数是用符号位扩展或者截断；无符号数0扩展或者截断。
+ 如果目标类型是signed，如果目标的值可以用相应的类型表示则值不变；否则结果是实现相关的。
+ 如果源类型是bool，false是0，true是1（如果目标类型是int，则是整型提升，不是整数转换）
+ 如果目标类型是bool，这是bool转换。


<a id="float_conversion"></a>
### 浮点转换
---


浮点类型的值可以转换任何其它的浮点类型。如果转换是按下述进行，那么是浮点提升，不是转换：

+ 源类型可以由目标类型精确表示，其值不变
+ 源类型表示成目标类型两个值之间的某个值，结果是两个值之一，是实现相关的。
+ 其它情况，未定义。


<a id="float_integer"></a>
### 浮点-整型转换
---


+ 浮点类型可以转换成任意的整型，小数部分直接被截断（直接丢弃）。如果截断后的值没法用目标类型表示，那么行为是未定义的。如果目标类型是bool，则是bool转换。
+ 整型或者unscoped枚举类型是可以转换任意浮点类型。如果其值无法精确表示，则由实现定义选择最接近最大值或者最小值来表示。如果其值无法用指定类型表示，行为未定义。如果源类型是bool，false是0，ture是1.


<a id="ptr_conversion"></a>
### 指针转换
---


+ 空指针是NULL常量，为0的整型值或者std::nullptr\_t类型，包括nullptr，可以转换成任意类型，结果是转换后类型的空指针。这种转换（又被称为空指针转换）可以一次变成cv修饰的类型，意思是说这不是数值类型转换和修饰符转换的组合。
+ 指向任意目标类型T（cv修饰是可选的）的指针可以转换成void（相同的cv修饰符）。所得类型在内存布局上一致的。如果原指针是空指针，则结果是相应类型的空指针。
+ 指向派生类类型的指针（cv修饰是可选的）可以转换成相应的基类类型（相同的cv修饰）。转换的结果是指向原来对象中subobject的基类部分的指针。空指针是转换成相应类型的空指针。


<a id="ptr_mem_conversion"></a>
### 指向成员指针的转换
---


+ 空指针是NULL常量值，值为0的整型值或者std::nullptr\_t类型，包括nullptr，可以转换成指向成员的指针，结果是指向相应类型的空指针。
+ 指向某类型T基类B成员的指针可以转换成相同类型T的派生类中的成员指针。如果B无法访问或者未定义或者D的虚基类或者是D基类的基类，转换是ill-formed（不会编译）。结果类型可以解引用为D对象，其可以访问D类中为B的subojbect。空指针还是转换成相应类型的空指针。


<a id="bool_conversion"></a>
## 布尔转换
---


整型、浮点、枚举、指针以及指向成员的指针类型可以转换成bool。0值（整型、浮点和枚举）以及空指针，指向成员的空指针转换成false，其它值是true。


<a id="cv_conversion"></a>
## 修饰符转换
---


+ 指向cv修饰符修饰的指针，可以转换为更多cv修饰符修饰的指针。
+ 指向cv修饰符修饰的成员类型的指针，可以转换更多cv修饰符修饰的指针。
+ 没有修饰符：增加const
+ 没有修饰符：增加volatile
+ 没有修饰符：增加const volatile
+ const修饰：变成 const volatile
+ volatile修饰：变成 const volatile


<a id="safe_bool"></a>
## 安全bool值问题
---


直到C++11中引入的显示转换，设计一个可以用在需要布尔值的上下文是一个问题：考虑用户自定义的转换函数，例如T::operator bool() const，隐式的转换顺序允许在函数调用后有额外的转换，即bool值可以转换为int，这样像obj<<1，或者 int i = obj是合法的。

早期的解决方法可以在std::basic\_ios中发现，它定义了operator!和operator void\*（直到c++11），所以当这样的代码：if(std::cin)编译成为void\*，然后转换成bool值，但是int n = std::cout不编译，因为void\*无法转换成int。但是这仍然允许一些奇怪的代码，例如 delete std::cout，在C++11之前的一些第三方库设计一些更加优雅的解决方法，称为<a href="http://www.artima.com/cppsource/safebool.html" target="_blank">Safe Bool idiom</a>
