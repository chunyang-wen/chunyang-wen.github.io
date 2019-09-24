---
layout: post
title: Python 中 Retrier 的实现
categories: [python]
tags: [python]
---

- [简介](#introduction)
- [两种 Retrier](#execute-hook)
  - [Retry with hook](#execute-hook)
  - [Retry with sleep and count](#retry-gap-count)

<a name='introduction'></a>

### 简介

最近工作中有个需求是当某个命令失败时，重新执行它。当然重新执行它有多重原因，例如：

+ 执行另外一个 hook 的函数
+ 由于网络等原因，希望等待的一定的间隔重试几次

本文介绍如何利用 `Python` 装饰器来实现

<a name='execute-hook'></a>

### Retry with hook

例如有个函数 `exec_cmd`, 由于可能存在缓存（.cache）会导致这个命令执行失败，所以希望清理缓存重试一次。

```python
from __future__ import print_function
import os
def exec_cmd(a, cache):
    if os.path.exsits('.cache'):
        print('Cache Hit')
        if CACHE_TOO_LONG:
            return -1
    else:
        print('Cache miss')
    return 0
```

如何让上述函数挂上我们的钩子呢？

```python
import subprocess
def clear_cache():
    subprocess.call('rm -rf .cache', shell=True)
```

根据 [Python 装饰器](https://www.chunyangwen.com/python/python-descriptor-decorator.html) 这篇文章
的描述，我们需要一个函数，接受一个钩子，然后返回一个装饰器。

```
def retry_with_hook(fn):
    def inner(fn_to_wrap): # decorator
        @functools.wraps(fn_to_wrap)
        def inner_most(*args, **kwargs): # decorated result function
            status = fn_to_wrap(*args, **kwargs)
            if status != 0:
                if callable(fn):
                    fn()
                    return fn_to_wrap(*args, **kwargs)
             return status
         return inner_most
    return inner
```

然后就可以给我们的函数进行装饰了

```python
from __future__ import print_function
import os
@retry_with_hook(clear_cache)
def exec_cmd(a, cache):
    if os.path.exsits('.cache'):
        print('Cache Hit')
        if CACHE_INVALID:
            return -1
    else:
        print('Cache miss')
    return 0
```

<a name='retry-gap-count'></a>

### Retry with sleep and count

通常的需求可能是根据一定的时间间隔重试几次。其装饰器如下：

```python
def retry_with_sleep_and_count(sleep_gap, count):
    def inner(fn_to_wrap):
        @functools.wraps(fn_to_wrap)
        def inner_most(*args, **kwargs):
            for i in range(count):
                try:
                    return fn_to_wrap(*args, **kwargs)
                except Exception as e:
                    time.sleep(sleep_gap)
        return inner_most
    return inner
```

本文完. Enjoy it.

+ Update at 2019-07-22, add `functools.wraps` to preserve infomation of original
