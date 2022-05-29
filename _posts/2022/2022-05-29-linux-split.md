---
layout: post
title: Linux split
categories: [blog, tools]
tags: [tools]
---

Linux 中有很多易用的命令行工具。`split` 就是其中之一。介绍实际中使用的几个比较常用的分割文件的方法。

+ toc
{:toc}

**Macos** 中的 `split` 命令和 `linux` 行为不太一致。

## 按照固定行切分

```bash
split -a 4 -l 1234 -d file.txt prefix_
```

+ -a 使用后缀的长度是 4 个位置
 + `-x` 使用 16 进制
+ -l 文件行数为 1234
+ -d 使用数字的后缀

按照固定的行数来进行切分。这种情况一般我们会使用 `wc -l` 来进行行数统计。

## 自动切分行

```bash
split -d -n l/10 output output_
```

使用数字后缀，将 `output` 切换成 10 个文件，文件的前缀是 `output_`。

## 切分文件的方式

+ `-l`: 按行
+ `-b`: 按照 bytes
+ `-n`: 按照 chunk 的方式
  + `N`: 按照 bytes 切分位 N 个文件
  + `K/N`: 只输出第 K 个 part
  + `l/N`: 按照行切分为 N 个文件
  + `l/K/N`: 按照行切分为 N 个文件，只输出第 K 个。
  + `r/N`, `r/K/N`: 按照 round-robin 方式来进行输出

## Reference

+ [Split](https://man7.org/linux/man-pages/man1/split.1.html)
