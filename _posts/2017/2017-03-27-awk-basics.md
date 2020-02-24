---
layout:     post
title:      awk 基本概念
categories: [blog, shell]
tags: [shell]
redirect_from:
 - /linux/awk/awk-basics
---


`Linux` 下的神器除了 `sed`，就有 `awk`。平时工作中 `awk` 可能相对更加强大。但是术业有专攻，不同工具
根据使用场景的不同会有不同的作用。本文将介绍 `awk` 的一些基本概念以及 `awk` 在处理字符串上的一些函数。


### awk 基本概念

`awk` 分为三个块：

```shell
BEGIN {

}
{}
END {

}
```

+ BEGIN块，`awk` 会保证在所有语句执行前执行。一般用于一些变量的初始化或者配置读取等
+ 执行块，执行块是针对每一行的文本都处理。我们可以利用条件来过滤待处理的行，跳过不关心的行
+ END块，`awk` 会保证在所有语句执行结束后执行。一般用于最后结果的汇总输出。

### awk 基本变量

`awk` 在解析每一行文本时会修改很多预定义的变量，这些变量的值对我们处理文本的行非常重要。

+ FS: 如何切分文本
+ OFS：输出文本时，如果将各列拼接乘一行
+ RS/ORS：确定文本之间的行
+ NF：所处理行的列数
+ NR/FNR：目前处理的行数，FNR表示当前文件的行数。因为 `awk` 可以同时处理多个文件
+ OFMT：定义输出数值时的格式
+ $0~$NF：$0表示整行，$1~$NF表示利用 FS 切分后行的各列
+ ARGC, ARGV
+ ARGIND：输入文件的需要：awk -f test.awk file1 file2， ARGIND==1表示file1
+ FILENAME：当前处理的文件名
+ ENVIRON["name"]：获取系统当前名为`name`的环境变量
+ system: 执行系统命令, system("ls")

### awk 数据类型

+ 整型: 可以通过函数 `int()` 进行转换
+ 浮点型
+ 数组：关联数组/顺序数组
+ 函数
+ 字符串：通过算数有关的运算变成数值类型

#### 数值（整型和浮点型）

```shell
# save as test.awk
BEGIN {
	a = 1;
	b = 2.3;
	c = "1.8";
	d = a""b;
	e = b + c;
	f = int(b);
	print a, b, c, d, e, f;
}

awk -f test.awk

# output
1 2.3 1.8 12.3 4.1 2
```

其中浮点型的输出 `printf` 支持和 c 语言类似的格式描述。

#### 数组

数组是常用的数据结构。如果索引是连续的整数，则类似于 `array`，如果数组的索引是其它的值，则类似于
`dict`。

```shell
# save as test.awk
BEGIN {
	a[0] = 1;
	a[1] = 2;
	b["hi"] = "world";
	print a[0], a[1], b["hi"]
}
awk -f test.awk
# output
1 2 world
```

判断元素是否在数组中：

```shell
BEGIN {
	a[0] = 1;
	a[1] = 2;
	if (0 in a) {
		print "Exists";
	}
}

```

数组排序：使用升序排序，可以排序索引值或者数值。

注意索引的起始值为 `1`。

+ slen = asort(a, b)：排序数组的值，将值存入数组 b
+ slen = asorti(a, b)：排序数组的索引，将下标存入数组 b

```shell
BEGIN {
	a["z"] = 34;
	a["b"] = 12;
	# sort values
	slen = asort(a, b);
	for (i = 1; i <= slen; ++i) {
		print b[i];
	}

	# sort indexes
	slen = asorti(a, b);
	for (i = 1; i <= slen; ++i) {
		print b[i];
	}
}
```

遍历数组：注意通常 `awk` 的函数在处理问题时返回数组时都是以 `1` 为起始索引。例如 `split`。

```shell
BEGIN {
	a[0] = 1;
	a['hi'] = "world";
	for (key in a) {
		print key" : "a[key];
	}
	b[0] = 1;
	b[1] = 2;
	for (i = 0; i < 2; ++i) {
		print i" : "b[i];
	}
}
```

多维数组

`awk` 默认不支持多为数组，但是可以通过类似的方式来实现。

```shell
BEGIN {
	a["hi", "world"] = 1;
	a["world", "hi"] = 2;
	for (key in a) {
		split(key, b, SUBSEP);
		print b[1], b[2], a[b[1], b[2]];
	}
}
```

#### 函数

`awk` 中的函数和 `c` 语言中的函数类似。关键字 `function`，不同于强类型函数，其可以返回任意类型的值。

可惜`awk` 中的函数不是一等公民，其不可以像变量一样来回传递。

```shell
# save as test.awk
function fact(n) {
	if (0 == n || 1 == n) {
		return "1";
	}
	return n * fact(n-1);
}

BEGIN {
	print fact(2);
	print fact(4);
}
```

#### 字符串

字符串是任何一门语言都要能有效地处理的类型。`awk` 支持一些常用的函数，下面重点介绍4种类型的操作：

+ 长度
+ 拼接
+ 切分
+ 替换

字符串和正则表达式将在下一篇文章中具体介绍。

本文完
