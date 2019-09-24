---
layout:     post
title:      awk内置函数和字符串
categories: [blog, shell]
tags: [shell]
---


本文主要介绍 `awk` 的内置函数以及字符串相关的处理函数。

### 内置函数

内置函数主要是数学相关的运算函数。

|函数名|函数功能|
|------|--------|
|atan2| 计算y/x 反正切值|
|cos|cos值|
|sin|sin值|
|sqrt|求平方根|
|log|自然数为底|
|int|强制转换为整型|
|rand|rand()，返回0<= n < 1的值|
|srand|srand(seed)，以seed为种子|

### 字符串相关的函数

#### 转换为字符串

+ 与"" 拼接
+ 使用 `sprintf(format-str, expr, expr)`，返回格式化的字符串
+ tolower/toupper，大小写转换

#### 字符串匹配/替换/查找函数

|函数名字|函数原型以及含义|
|--------|----------------|
|index|index(src, pattern), 返回指定pattern的位置，注意0表示未找到，非0表示位置|
|sub|sub(pattern, replacement, src)，返回替换的数目|
|gsub|gsub(pattern, replacement, src)，替换所有的查找项|
|match|match(src, pattern)，RSTART，RLENGTH，返回0表示未找到|
|length|字符的个数|
|blength|byte的个数|

### 其它函数

+ getline
  + getline variable-name：读入下一行到variable-name变量
  + getline < variable-name：将variable-name读入$O
  + getline：将下一行读入$0
+ close
+ system("command")：执行 shell 命令
+ 时间相关的：
  + mktime：mktime( YYYY MM DD HH MM SS[ DST ] ), mktime("2010 11 01 00 00 00")
  + strftime(format, timestamp)：timestamp可以由下面函数生成
  + systme()：返回1970-01-01到现在的整秒数

|格式|描述|
|----|----|
|%a|星期几的缩写(Sun)|
|%A|星期几的完整写法(Sunday)|
|%b|月名的缩写(Oct)|
|%B|月名的完整写法(October)|
|%c|本地日期和时间|
|%d|十进制日期|
|%D|日期 08/20/99|
|%e|日期，如果只有一位会补上一个空格|
|%H|用十进制表示24小时格式的小时|
|%I|用十进制表示12小时格式的小时|
|%j|从1月1日起一年中的第几天|
|%m|十进制表示的月份|
|%M|十进制表示的分钟|
|%p|12小时表示法(AM/PM)|
|%S|十进制表示的秒|
|%U|十进制表示的一年中的第几个星期(星期天作为一个星期的开始)|
|%w|十进制表示的星期几(星期天是0)|
|%W|十进制表示的一年中的第几个星期(星期一作为一个星期的开始)|
|%x|重新设置本地日期(08/20/99)|
|%X|重新设置本地时间(12：00：00)|
|%y|两位数字表示的年(99)|
|%Y|当前月份|
|%Z|时区(PDT)|
|%%|百分号(%)|

本文完
