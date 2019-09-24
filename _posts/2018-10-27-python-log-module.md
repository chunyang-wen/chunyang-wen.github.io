---
layout: post
title: Python logging module
categories: [blog, python]
tags: [python]
---

+ [简介](#intro)
+ [基本打印日志](#normal-print)
+ [高级用法](#advanced-usage)
  + [区分系统日志和用户的日志](#system-and-user)
  + [多个目标输出](#file-stdout-stderr)
  + [对日志进行过滤](#filter-log)
  + [对日志进行 format](#format-again)

<a id="intro"></a>

### 简介

日志对于任何一个工程来说都是非常重要的，它分为多个级别。一般分为如下级别：

+ DEBUG
+ INFO
+ WARN
+ ERROR

当然不同的日志模块划分可能不一定一致，但是基本都是分 LEVEL 来输出日志。本文简单介绍下 Python 的日志
模块。主要是在平常使用过程中的一些问题和技巧。

<a id = "normal-print"></a>

### 基本打印日志

Python 中的打印日志模块是 `logging`, 其默认的输出 `LEVEL>=WARN`

```python
import logging
logging.warn('I warn you!')
```

可以看到这日志的输出比较简单，没有例如行号，时间，所在的函数名字等信息。格式配置如下：

|Attribute name|Format|Description|
|--|--|--|
|asctime|	%(asctime)s	|Human-readable time when the LogRecord was created. By default this is of the form ‘2003-07-08 16:49:45,896’ (the numbers after the comma are millisecond portion of the time).|
|created|	%(created)f	|Time when the LogRecord was created (as returned by time.time()).|
|filename|	%(filename)s	|Filename portion of pathname.|
|funcName|	%(funcName)s	|Name of function containing the logging call.|
|levelname	|%(levelname)s	|Text logging level for the message ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').|
|levelno|	%(levelno)s	|Numeric logging level for the message (DEBUG, INFO, WARNING, ERROR, CRITICAL).|
|lineno	|%(lineno)d	|Source line number where the logging call was issued (if available).|
|module	|%(module)s	|Module (name portion of filename).|
|msecs	|%(msecs)d	|Millisecond portion of the time when the LogRecord was created.|
|message|	|%(message)s	The logged message, computed as msg % args. This is set when Formatter.format() is invoked.|
|name	|%(name)s	|Name of the logger used to log the call.|
|pathname	|%(pathname)s	|Full pathname of the source file where the logging call was issued (if available).|
|process	|%(process)d	|Process ID (if available).|
|processName|	%(processName)s	|Process name (if available).|
|relativeCreated	|%(relativeCreated)d	Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded.|
|thread	|%(thread)d	|Thread ID (if available).|
|threadName	|%(threadName)s	|Thread name (if available).|


```python
import logging
logging.basicConfig(format='[%(levelname)s]:%(message)s', level='INFO')
logging.info('SayHi')
```

> If we set filename or stream parameter of `basicConfig`, we will be able to output to specific file or stream

<a id="advanced-usage"></a>

### 高级用法

上述的做法对于只有一种打印需求来说没有什么问题。如果出现如下情况：

+ 需要区分系统打印的日志和用户自己打印的日志
+ 用户想对日志完成比较复杂的过滤
  + 如果出现敏感内容：替换成通用的字符，例如密码替换成 password
+ 不同日志来源打印的格式不一致
+ 日志同时输出到文件和终端

以上问题直接使用 `logging` 模块是存在问题的。下面我们看 `logging` 模块怎么解决上述问题。

<a id="system-and-user"></a>

#### 区分系统日志和用户的日志

`logging` 模块有个接口 `getLogger`，其支持传入一个 logger 的名字。这个是单例的，如果名字存在则返回对应的对象，否则创建一个新的。我们只要系统使用的 logger 名字是唯一的即可。

```python
import logging
import sys

logger1 = logging.getLogger('TestLogger1')
logger2 = logging.getLogger('TestLogger2')
handler = logging.StreamHandler(stream=sys.stderr)
formatter = logging.Formatter('%(name)s:%(message)s')
handler.setFormatter(formatter)
handler.setLevel(logging.getLevelName('DEBUG'))
logger1.addHandler(handler)

handler2 = logging.StreamHandler(stream=sys.stderr)
formatter = logging.Formatter('%(name)s:%(message)s')
handler2.setFormatter(formatter)
handler2.setLevel(logging.getLevelName('DEBUG'))

logger2.handlers = [handler2]

logger1.setLevel('INFO')
logger2.setLevel('DEBUG')

logger1.info('I am TestLogger1')
logger2.info('I am TestLogger2')
```

> 每个 logger 都有自己的 Level，通过 handler 来限制，只能从 >= logger 的 level 才会
> 生效。例如 handler 的 level = debug，但是 logger 的 level = info，这个时候 debug
> 日志仍然不会输出给 handler

只要保证系统在打印日志时，不要和普通用户使用同样的 `logger` 即可。而且在创建`logger` 的格式上完全
可以自定义。其主要就是通过不同的 `handler` 来实现的。

+ `addHandler(handler)`
+ `logger.handlers = [handler1, handler2]`

建议使用第一种方式，利用 API 来完成添加。

<a id="file-stdout-stderr"></a>

#### 多个目标输出

框架希望将日志不仅输出到终端，也希望输出到文件，而且希望文件可以按照时间或者大小来切分，这些都可以通过增加不同的 `handler` 来实现

+ `StreamHandler(stream=None)`
  + stream 可以取值为：`sys.stderr`, `sys.stdout`
+ `FileHandler(filename, mode='a', encoding=None, delay=False)`
  + 将日志输出到某个文件
+ WatchedFileHandler: 类似 FileHandler
  + 检测对应文件是否有改变，有的话会关闭重新打开
+ `RotatingFileHandler(filename, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0)`
  + 将日志输出到文件，且文件会切割
+ TimedRotatingFileHandler

还有一些其他的，请参考 Python 官方的文档

```python
import logging
import sys

logger = logging.getLogger('multi-output-logger')
logger.setLevel('INFO')

fh = logging.FileHandler('test.log')
format_fh = logging.Formatter('%(name)s:%(asctime)s:%(message)s')
fh.setFormatter(format_fh)

ch = logging.StreamHandler(stream=sys.stderr)
format_ch = logging.Formatter('%(name)s:%(levelname)s:%(message)s')
ch.setFormatter(format_ch)

logger.addHandler(fh)
logger.addHandler(ch)

logger.info('Tell me')
```

<a id="filter-log"></a>

#### 对日志进行过滤

通过 `handler` 的 `filter` 来实现的。

```python
import logging
import sys

logger = logging.getLogger('test-logger')
logger.setLevel('DEBUG')
handler = logging.StreamHandler(stream=sys.stderr)
formatter = logging.Formatter('%(name)s-%(levelname)s-%(message)s')

filter_log = logging.Filter(name='test-logger')
def func(record):
    # record 的 attributes 可以参考上面的表格
    if record.msg.startswith('hell'):
        return 0
    return 1
filter_log.filter = func

handler.setFormatter(formatter)
handler.addFilter(filter_log)
logger.addHandler(handler)

logger.info('hi')
logger.info('hello')
```

<a id="format-again"></a>

#### 对日志进行 format

默认我们可以通过 `Formatter` 函数来对日志进行格式化。但是有时候我们想对日志完成细粒度的控制：

+ 对于敏感内容不是直接把整条日志给过滤，而是将敏感内容通过字符替代
+ 我们有更加高级的自定义需求，例如根据环境变量来控制日志的内容等

简单带你我们可以重载 `Formatter` 的 `format` 函数。例如下面是过滤日志中出现 `password`，然后替换为简单的字符。

```python
import logging
import sys

logger = logging.getLogger('format-logger')
logger.setLevel('INFO')

formatter = logging.Formatter('%(name)s:%(msg)s')

def update_format(func):
  def inner(*args, **kwargs):
    msg = func(*args, **kwargs)
    import re
    return re.sub(r'password=\S+', 'password=^_^', msg)
  return inner

formatter.format = update_format(formatter.format)

handler = logging.StreamHandler(stream=sys.stderr)
handler.setFormatter(formatter)

logger.addHandler(handler)

logger.info('user=zhang.san password=zhang.san123')
```

本文完
