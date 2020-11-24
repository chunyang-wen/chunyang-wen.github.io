---
layout: post
title: Estimator core in evaluator
categories: [blog, tensorflow]
tags: [tensorflow]
---

记录另外一次 Estimator 的 core 排查。

+ toc
{:toc}

## 背景

我们用户使用 Estimator 都是使用 chief + worker + ps + evaluator 的形式。在线上偶发的 evaluator 这个角色会 core 掉。


```bash
NotFoundError: ** open file failed **
***Error in `python`: malloc: smallbin double linked list corrupted***
```

打开文件失败，打开的是 `CheckpointSaverHook` 写出 checkpoint 时写出的 checkpoint state 文件。这个 checkpoint state 文件存储最新的模型版本和文件的路径信息。每次保存模型时，都会去更新它。 为了保证正确性，tensorflow 是会先写临时文件，再写 rename 成目标文件。

这里存在一种可能是：chief 保存模型时在 rename 一瞬间，evaluator 先读，然后 close 失败。

由于我们写的是一个分布式系统（类似于 HDFS）。rename 不是原子的，会先删除，然后在 rename。线下尝试复现这个问题，一直没有复现成功。

今天另外一个同事也遇到了这个问题，问题的严重性凸显。因为 core 的日志还显示不全。

## 复现代码

写了两个脚本

模拟 evaluator 的功能，不断地去读 `checkpoint` 文件，以获取 state。

```python
import time
import random

import tensorflow as tf
from tensorflow.python import file_io

path = "/path/to/file.txt"

while True:
    try:
        with tf.gfile.Open(path) as fd:
            print(fd.read())
        seconds = random.random() * 3
        print("sleep: ", seconds,  " s")
    except Exception as e:
        print(e)
    time.sleep(seconds)
```

模拟 chief 的行为，不停地去写 checkpoint 文件。

```python
import time
import random

import tensorflow as tf
from tensorflow.python import file_io

path = "/path/to/file.txt"

while True:
    file_io.atomic_write_string_to_file(path, contents)
    seconds = random.random() * 3
    print("sleep: ", seconds,  " s")
    time.sleep(seconds)
```

一段时间后就发现 core 了。很开心，终于可以稳定复现。

```bash
ulimit -c unlimited  # enable core file
cat /proc/sys/kernel/core_pattern  # core file location
gdb python -c /path/to/core_file
```

通过允许 core，以及 core 的位置。将 core 给相关存储 RD 排查，怀疑是文件句柄被重复 close。

仔细 Review 之前的 code，发现之前在修复 tensorflow 的一个问题时，读到 bytes 为 0，但是文件没有结束时，
会关闭文件，然后重新打开文件。在这个期间如果文件被删除，打开会失败。会走到 File 类的析构函数，在析构
函数中会再次关闭文件，由于第一次关闭文件时并没有置空句柄，导致重复关闭时 core。

## Lessons learned

+ 出现 core 时，需要尽量知道 core 发生的路径，例如特殊数据，特殊逻辑。然后在线下复现
+ C++ 中对于句柄的管理，析构很重要。还是最好交由智能指针来做

## 参考

+ [Checkpoint Management](https://github.com/tensorflow/tensorflow/blob/v1.15.0/tensorflow/python/training/checkpoint_management.py#L245)
+ [file\_io](https://github.com/tensorflow/tensorflow/blob/v1.15.0/tensorflow/python/lib/io/file_io.py#L522:5)
+ [Tensorflow #5438](https://github.com/tensorflow/tensorflow/issues/5438)
