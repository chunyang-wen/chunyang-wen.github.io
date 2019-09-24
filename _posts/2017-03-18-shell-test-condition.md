---
layout: post
title: Linux shell 条件判断
categories: [blog, shell]
tags: [shell]
---


Linux shell 编程的条件判断主要使用

```shell
if [ condition ]; then
# your statements
fi
```

+ 注意 condition 左右是要有空格的，不然会得到如下的错误。有时候会被错误信息弄的莫名其妙。

```shell
[ $a -eq 1] # miss tailing zero
[: missing `]''`]

[$a -eq 1 ] # miss leading zero
[: -eq: unary operator expected]
```

+ 注意如果使用变量，使用""将变量包裹起来，放置被shell扩充后造成混淆。

```shell
a="11 11"
if [ -z $a  ] # not wrap using ""
then
    echo 'hh'
fi
[: 11: binary operator expected]
```

上述的错误是因为 `$a` 被展开成实际的 `11 11`，但是没有用双引号扩起来实际上条件是：

```shell
-z 11 11
```

`shell` 本身支持很多的内置条件，主要分为三类：

+ 文件相关的：文件是否存在，文件属性等
+ 字符串相关的
+ 数字相关的

### 文件相关的

+ [ -b file ] file是块设备文件
+ [ -c file ] file是字符设备文件
+ [ -f file ] file为一般文件
+ [ -g file ] file有设置它的setgid位
+ [ -h file ] file是一符号连接
+ [ -L file ] file是一符号连接，等同于-h
+ [ -p file ] file是管道文件
+ [ -S file ] file是Socket文件
+ [ -s file ] file是空文件
+ [ -d file ] file是目录
+ [ -e file ] file存在
+ [ -r file ] file可读
+ [ -w file ] file可写
+ [ -x file ] file可执行

#### 字符串相关的

+ -z string: 判断字符串是否为空
+ -n string: 判断字符串是否非空
+ s1 = s2 : 相等
+ s1 == s2 : 相等
+ s1 != s2 : 不相等

字符串的其它比较一般放在`[[  ]]` 中。

+ [[ "$a" > "$b" ]]
+ [[ "$a" == z* ]] : 正则匹配的比较
+ [[ "$a" == "z*" ]]: 字面的比较

### 数字相关的

+ n1 -eq n2
+ n1 -lt n2
+ n1 -le n2
+ n1 -gt n2
+ n1 -ge n2
+ n1 -ne n2

### 表达式的组合

+ -a: 与
+ -o: 或
+ ! : 非

上述实例如下：

```shell
if [ n1 -eq n2 -a n3 -gt n4 ]
then
    echo "do something"
fi
if [ n1 -eq n2 -o n3 -gt n4 ]
then
    echo "do something"
fi

if [ ! -e file ]
then
    echo "File not exist"
fi
```

### Linux 命令作为条件

`Linux` 下很多的命令执行成功返回0，执行失败返回非0。如果需要根据命令的执行情况来决定下一步要进行
的操作。

```shell
# test.txt中有两行文本：
# hi
# hello

grep "hi" test.txt

if [ $? -eq 0 ]
then
    echo "Success."
fi
```

`$?` 表示上次命令的返回值。实际上可以直接直接使用如下形式：

```shell
if grep "hi" test.txt &>/dev/null
then
    echo "Success."
else
    echo "Failed"
fi
```

### 结合 &&, ||, (cmd1, cmd2)

当某个条件为真时，需要执行某些操作。使用 `if` 当然可以完成所有工作，但是除了写条件，还要写 `if`，
`fi`，`then`，比较多。利用 `Linux` 短路的操作，可以方便完成上述功能。

```shell
[ -e file ] && echo "File found"
[ ! -e file ] && echo "File not found"
```

### 其它

+ `[ condition ]` 可以替换为 `test condition`，`test` 是 `shell` 关键字

本文完
