---
layout: post
title: iostream用法
categories: [blog, cpp]
tags: [cpp]
---


iostream是C++中一个比较复杂的库，其设计的时候还应用了为人所诟病的钻石继承。在GoNative大会上，有人提问iostream那么复杂，而且相对于C的库函数，其效率相对低，为什么还要将其一直留在标准中。这个问题得到了如下回答（个人总结）：

![iostream.gif](/images/iostream.gif "iostream inheritance")

>C++中的iostream是安全的；目前没有库可以取代iostream。

相对于C，iostream做了很多封装，但是其结果是为用户提供类型安全。在C++中cin和cout分别是istream和ostream的实例。

```cpp
extern istream cin;
typedef basic_istream<char, char_traits<char> > istream;

extern ostream cout;
typedef basic_ostream<char, char_traits<char> > ostream;
```

通常我们使用的头文件<iostream/>，其中包含如下流对象的定义：

+ cerr/wcerr
+ cin/wcin
+ clog/wclog
+ cout/wcout

由于cin/cout分别是istream和ostream类型的变量，而istream和ostream分别是basic\_istream和basic\_ostream的typedef，接下来看看basic\_istream和basic\_ostream中的成员变量和函数：

1. basic\_istream
	+ basic\_istream构造函数     
		```cpp
		explicit basic_istream( basic_streambuf<Elem, Tr> *_Strbuf, bool _Isstd = flase);
		```     
	+ streamsize gcount() const，返回上一次读入的字节数
	+ get，读入一个字符
	+ getline，读入一行字符
	+ ignore(streamsize \_Count=1, int\_type \_Delim = traits\_type::eof());
	+ peek，返回下一个将被读取的字符，但是流的位置不前进
	+ putback，将一个指定字符放入流中
	+ read(char\_type \*\_str, streamsize \_count)，从流中读入指定长度的字节，存入数组
	+ seekg(pos\_type \_Pos), seeg(off\_type \_off, ios::base::seekdir \_way);
	+ sync()，将流与缓冲结合
	+ tellg()，返回位置
	+ unget()，将最近读取的字符退回流
	+ operator\>\>
2. basic\_stream中的成员
	+ basic\_stream构造函数
	+ flush，刷新缓冲区
	+ seekp
	+ tellp
	+ write(const char\_type \*\_str, streamsize \_cnt)
	+ operator<<
3. basic\_ios成员
	+ basic\_ios构造函数
	+ bad
	+ clear
	+ copyfmt
	+ eof
	+ exceptions
	+ fail
	+ fill
	+ good
	+ imbue
	+ init， 调用basic\_ios构造函数
	+ narrow
	+ rdbuf
	+ rdstate
	+ setstate
	+ tie: 确保某个流在另一个流之前已经处理
	+ widen
	+ operator void\* 指示流是否仍然处于好的状态
	+ operator! 指示流是否不坏

上面了介绍istream和ostream的一些成员函数，其中忽略了一些typedefs。

C++中输入输出流使用cin/cout，其相对于C的scanf和printf更加安全，但是同时也导致其效率相对低。

四个设置函数在头文件\<iomanip\>中。

1. 整形数输出格式控制
    + boolalpha, noboolalpha：在输出true/false时，是numeric（0, 1）还是literal（true, false）。

```cpp
bool is_good = false;
std::cout<<std::boolalpha<<is_good<<std::endl;
std::cout<<std::noboolalpha<<is_good<<std::endl;
```
+ showbase/noshowbase：显示表示整数的基，0X，0等。
+ hex/oct/dec：显示输出的进制。 16进制中x的大小写，uppercase/lowercase 
    
```cpp
int a = 0x36;
std::cout<<std::dec<<a<<std::oct<<a<<std::hex<<a<<std::endl;
```

以上功能改变都是持续性的，直到改变回原样为止。

2. 浮点数格式化输出
    + setw(int), setprecision(int), setfill(char), setbase(8/10/16)：这三个函数分别是设置输出的宽度，精度以及当宽度不足时的补充和输出的基数。
    + showpoint/noshowpoint：设置输出小数位是0的浮点数时是否强制显示小数位的0。
    + left/right/internal：设置在setw后当宽度小于设置的值时的填充位置。internal输出有符号数时，左移符号位，右移数字，在中间填充字符。
    + cout.unsetf(ostream::floatfield)：恢复到初始状态，有效数字为6位。
    + fixed/scientific：fixed固定输出小数点后6位

```cpp
#include <iostream>
#include <iomanip>

int main()
{
	std::ios::fmtflags flags(std::cout.flags());
	int a = 3;
	// fill 0, default: fill '', right align;
	std::cout<<std::left<<std::setw(3)<<std::setfill('x')<<a<<std::endl;
	double b = 3.123;
	// output two effective numbers after decimal point
	std::cout<<std::fixed<<std::setprecision(2)<<b<<std::endl; 
	std::cout.flags(flags);
	// output 2 effective number
	std::cout<<std::setprecision(2)<<b<<std::endl; 
}
```

会导致流刷新的事件：

+ 缓冲区满。
+ 在输出流之后有输入操作，立即刷新缓冲区
+ 使用相关运算子或者函数主动刷新流。
	+ 使用 endl 操控器的输出流中插入一个换行符，并刷新缓冲区。与 endl 的操控，使用插入运算符，如下所示：
        cout << ... << endl;
	+ 使用 ostream 类或刷新操控器中的刷新成员函数。齐平的操控程序不会流到插入换行符之前它刷新缓冲区。要调用的齐平的成员函数，请使用类似于以下代码：
        cout.flush();
	+ 齐平的操控与使用插入运算符，如下所示：
        cout << ... << flush;
	+ 从 cin 流中读取或写入 cerr 或 clog 的流。由于这些对象会与 cout 共享缓冲区，每对它进行任何更改之前刷新缓冲区的内容。
	+ 退出该程序以刷新当前正在使用的所有缓冲区。

参考文献：

1. <a href=http://msdn.microsoft.com/en-us/library/yeecc295%28v=vs.80%29.aspx target="_blank">MSDN iostream</a>
2. <a href=http://www.cplusplus.com/reference/iolibrary/ target="_blank">cplusplus.com,继承图出处</a>

本文完
