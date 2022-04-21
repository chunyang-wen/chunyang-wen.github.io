---
layout: post
title: Python itertools
tags: [blog, python]
categories: [python]
---

最近在工作中使用 python 开发时经常需要将多个 iterator 进行一些操作。以前的惯用手法要么是主动
使用 `for` 循环，要么是使用 `zip` 将多个 `iterator` 打平成多个。其实一直知道 `itertools` 这个库
的，这是偶尔会用，并没有去仔细研究过。

+ toc
{:toc}

## 合并多个文件

在开发中有如下需求：

> 将多个文件内容读出，但是对外感觉是一个文件

直观上我们可以使用，一次打开多个文件，调用 `next` 接口，如果出现 `StopIteration` 的异常，则
进入下一次循环。

```python
files = ["a.txt", "b.txt"]

for file in files:
    with open(file) as reader:
        for line in reader:
            print(line)
```

实际上我的需求更加多一点，我是 batch 形式的返回数据，所以还需要组装 batch。如果加入很多人工的
逻辑，确实也可以完成，但是会让代码看起来非常难看。

```python
class File:
    def __init__(self, files):
        self._files = files

    def __iter__(self):
        def func():
            for file in self._files:
                with open(file) as reader:
                    for line in reader:
                        yield line
        return func()



file = File(["a.txt", "b.txt"])

for line in file:
    line = line.strip()
    print(line)
```

假设 `a.txt` 和 `b.txt` 内容分别是

```bash
# a.txt
1
2
# b.txt
3
4
```

上述代码就会打印出

```bash
1
2

3
4
```

实际上借助 `itertools`，我们根本不需要这么麻烦

```python
from itertools import chain
files = ["a.txt", "b.txt"]
iterators = [open(file) for file in files]
handler = chain(*iterators)
for line in handler:
    print(line.strip())
```

## 合并多个文件 2

还是希望合并多个文件，但是不是像上文那样挨个顺序去合并，而是希望每次从一个文件取一个合并。

**多个文件内容不一定一致**

这个其实挺像 `zip` 功能的。

```python
files = ["a.txt", "b.txt"]
iterators = [open(file) for file in files]

for content in zip(*iterators):
    print(content)
```

但是 `zip` 有个问题，只要它的展开序列中任何一个停止，那么就会结束循环，某些 `iterator`
并不会全部取出。


```python
from itertools import zip_longest
files = ["a.txt", "b.txt"]
iterators = [open(file) for file in files]

for content in zip_longest(*iterators):
    print(content)
```

`zip_longest` 会一直输出，但是对于结束的 `iterator`，它对应的位置会填充上 `None`。所以在后面
还要增加一个 `filter` 操作，将所有的 `None` 过滤掉。

```python
v = list(filter(lambda v:v is not None, v))
```

## 间隔取行

本地多线程或者多进程处理一个文件时，如果我们按照某种 `index` 来对文件切分，例如存在 2 个
`worker`, 第一个 `worker` 读取 `0 2 4 ..` 行，第二个 `worker` 读取 `1 3 5...` 行。我们可以
自己维护一个计数器和一个 `worker_index`。针对不是自己的数据跳过。我就不贴实现了，其实 `itertools`
已经提供了一个工具来替我们完成这种切片操作。

假设 `c.txt` 中有如下数据

```bash
0
1
2
3
4
5
6
```

```python
from itertools import islice

worker_size = 3

reader = open("c.txt")
worker_index = 0
for data in islice(reader, worker_index, None, worker_size):
    print(data.strip())

reader = open("c.txt")
worker_index = 1
for data in islice(reader, worker_index, None, worker_size):
    print(data.strip())

reader = open("c.txt")
worker_index = 2
for data in islice(reader, worker_index, None, worker_size):
    print(data.strip())
```

用户只需要维护好自己的 `index` 和 `size` 即可。

## 其它内容

### 无穷尽的

+ `count(start=0, step1)`: 产出 counter
+ `cycle(p)`: 循环输出
+ `repeat(element, [n])`: ``

### 取数据

+ `takewhile(pred, seq)`
+ `dropwhile(pred, seq)`
+ `compress(seq, selectors)`

前两只要 `pred` 变为 `False`，相应的动作，`take` 或者 `drop` 就不会发生了。`compress` 有点类似
`select` 的功能。

### 其它

+ `tee(iterable, n=2)`: 一个复制为多个

```python
from itertools import tee

h = open("c.txt")
hs = tee(h, 3)

h = hs[0]
for data in h:
    print(data.strip())

h = hs[1]
```

+ `starmap(function, iterable)`: 期望 `iterable` 能够返回一个 `list`

## Reference

+ [Python itertools](https://docs.python.org/3/library/itertools.html)

还有很多其它有意思的实现，感兴趣的可以继续探索官方的样例。本文是支出在实际工作中作者用到的一些
比较有意思的函数。
