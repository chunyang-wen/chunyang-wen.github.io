---
layout: post
title: C++11中引入的ratio类
categories:
- programming
tags:
- ratio
---

C++11中引入了一个分数类，之前还没明白是怎么回事，看了内部的定义才明白是做什么的。我们首先将其代码贴出来。

```cpp
	namespace std {

		// class template ratio
		template <intmax_t N, intmax_t D = 1>
		class ratio {
		public:
			typedef ratio<num, den> type;
			static constexpr intmax_t num;
			static constexpr intmax_t den;
		};

		// ratio arithmic
		template <class R1, class R2> using ratio_add = /\* ratio \*/;
		template <class R1, class R2> using ratio_subtract = /\* ratio \*/;
		template <class R1, class R2> using ratio_multiply = /\* ratio \*/;
		template <class R1, class R2> using ratio_divide = /\* ratio \*/;

		// ratio comparison
		template <class R1, class R2> struct ratio_equal;
		template <class R1, class R2> struct ratio_not_equal;
		template <class R1, class R2> struct ratio_less;
		template <class R1, class R2> struct ratio_less_equal;
		template <class R1, class R2> struct ratio_greater;
		template <class R1, class R2> struct ratio_greater_equal;

		// convenience SI typedefs
		typedef ratio<1, 1000000000000000000000000> yocto;
		typedef ratio<1,    1000000000000000000000> zepto;
		typedef ratio<1,       1000000000000000000> atto;   
		typedef ratio<1,          1000000000000000> femto;  
		typedef ratio<1,             1000000000000> pico;   
		typedef ratio<1,                1000000000> nano;   
		typedef ratio<1,                   1000000> micro;  
		typedef ratio<1,                      1000> milli;  
		typedef ratio<1,                       100> centi;  
		typedef ratio<1,                        10> deci;   
		typedef ratio<                       10, 1> deca;   
		typedef ratio<                      100, 1> hecto;  
		typedef ratio<                     1000, 1> kilo;   
		typedef ratio<                  1000000, 1> mega;   
		typedef ratio<               1000000000, 1> giga;   
		typedef ratio<            1000000000000, 1> tera;   
		typedef ratio<         1000000000000000, 1> peta;   
		typedef ratio<      1000000000000000000, 1> exa;    
		typedef ratio<   1000000000000000000000, 1> zetta;
		typedef ratio<1000000000000000000000000, 1> yotta;
	}
```

代码不是很长， 主要是包括一个简单的声明以及一些宏定义。对于布尔值的运算结果，我们只需提取其value值即可。

```cpp
	ratio_less<ratio<1,10>, ratio<1,11> >::value // true or false
```

对于运算的结果，我们需要提取其num（分子），den（分母）即可。

```cpp
	ratio_add<ratio<1,10>, ratio<1,11> >::num // 分子
	ratio_add<ratio<1,10>, ratio<1,11> >::den // 分母
```

参考文献：

+ <a href=en.cppreference.com/w/cpp/header/ratio target="_blank"> Ratio</a>

<本文完\>
