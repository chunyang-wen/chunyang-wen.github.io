---
layout: post
title: Date and string format in python
categories: [blog, python]
tags: [python]
---

在 Python 中生成字符串有 3 种方式，现在比较建议的是使用 `f-str` 的方式，官方说性能更加好。本文主要
介绍在格式化时有哪些格式可以选择。

+ toc
{:toc}


## String

### %

```python
a = 42
b = "%d" % a

c = "answer to everything"
d = "%s %s" % (b, c)
```

### `format`

```python
a = "{} {}"
b = 1
c = 2
d = a.format(b, c)

a = "{bb} {cc}"
d = a.format(bb=b, cc=c)

person = {"first": "zhang", "last": "san"}
d = "{p[first]}-{p[last]}".format(p=person)

a = "{1} {0}"
d = a.format(b, c)  # 交换位置
```

## f-str

基本上所有的 `format` 支持得做法 `f-str` 都是支持的。这里展开介绍下具体的格式。

### 进制转化

```python
a = 13
print(f"{a:o}")
print(f"{a:b}")
print(f"{a:x}")
print(f"{a:d}")

b = 88.3998128733

print(f"{b:.4f}")
print(f"{b:.4e}")  # 科学技术法
```

### 对齐

```python
a = 13

print(f"{a:04}")   # 默认填充左边

# 自定义填充字符
print(f"{a:_>04}") # 填充左边
print(f"{a:_<04}") # 填充右边
print(f"{a:_^04}") # 填充左右
```

## benchmark

```python
python -m timeit "a=1;b=f'{a}'"
# 2000000 loops, best of 5: 102 nsec per loop

python -m timeit "a=1;b='{a}'.format(a=a)"
# 1000000 loops, best of 5: 336 nsec per loop
```

可以看出 `f-str` 比 `format` 的性能还是高不少。

## time format

```python
from datetime import datetime as dt

now = dt.now()

format = "%Y-%m-%d %H:%M:%S %a"

print(now.strftime(format))
```

|Code|Example|Description|
|:--|:--|:--|
|%a|Sun|Weekday as locale’s abbreviated name.|
|%A|Sunday|Weekday as locale’s full name.|
|%w|0|Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.|
|%d|08|Day of the month as a zero-padded decimal number.|
|%-|8|Day of the month as a decimal number. (Platform specific)|
|%b|Sep|Month as locale’s abbreviated name.|
|%B|September|Month as locale’s full name.|
|%m|09|Month as a zero-padded decimal number.|
|%-|9|Month as a decimal number. (Platform specific)|
|%y|13|Year without century as a zero-padded decimal number.|
|%Y|2013|Year with century as a decimal number.|
|%H|07|Hour (24-hour clock) as a zero-padded decimal number.|
|%-H|7|Hour (24-hour clock) as a decimal number. (Platform specific)|
|%I|07|Hour (12-hour clock) as a zero-padded decimal number.|
|%-||7|Hour (12-hour clock) as a decimal number. (Platform specific)|
|%p|AM|Locale’s equivalent of either AM or PM.|
|%M|06|Minute as a zero-padded decimal number.|
|%-M|6|Minute as a decimal number. (Platform specific)|
|%S|05|Second as a zero-padded decimal number.|
|%-S|5|Second as a decimal number. (Platform specific)|
|%f|000000|Microsecond as a decimal number, zero-padded on the left.|
|%z|+0000|UTC offset in the form ±HHMM[SS[.ffffff]] (empty string if the object is naive).|
|%Z|UTC|Time zone name (empty string if the object is naive).|
|%j|251|Day of the year as a zero-padded decimal number.|
|%-j|251|Day of the year as a decimal number. (Platform specific)|
|%U|36|Week number of the year (Sunday as the first day of the week) as a zero padded decimal number. All days in a new year preceding the first Sunday are considered to be in week 0.|
|%W|35|Week number of the year (Monday as the first day of the week) as a decimal number. All days in a new year preceding the first Monday are considered to be in week 0.|
|%c|Sun Sep 8 07:06:05 2013	Locale’s appropriate date and time representation.|
|%x|09/08/13|Locale’s appropriate date representation.|
|%X|07:06:05|Locale’s appropriate time representation.|
|%%|%|A literal '%' character.|

## Reference

+ [PyFormat.info](https://pyformat.info)
+ [Strftime.org](https://strftime.org)
