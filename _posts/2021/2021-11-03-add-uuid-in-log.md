---
layout: post
title: Add Unique ID for Http Request
categories: [blog, python]
tags: [python]
---

后端服务的每一次请求会进入各种逻辑，发生各种问题。在大并发情况下，不同请求之间的
日志还会混在一起。

+ toc
{:toc}

## 背景

为了便于查找和分析问题， 一般我们需要识别每一次请求。有两种方式：

+ 用户请求都会有唯一的 id，例如支付宝任何请求都会带上一个用户唯一的 id
+ 请求到达服务时，会有一个统一的唯一的 id 生成给这次请求。后续系统内部所有的流动都会带
上这个 id。

我们希望每次的日志打印都可以带上这个 id，这样我们通过这个 id 就可以检索出所有相关的日志。

## 唯一的 id

在 Python 中唯一的 id 生成一般使用 `uuid` 这个模块。

```python
import uuid

uid = str(uuid.uuid4())
```

`uuid4` 是其中的一种方法(有 1-5 几种方法)，可以根据自己的需求采取。这个 uid 再配合上一些其它策略，
例如机器编号，ip 地址等就可以保证 uid 是全局唯一的。uid 的缺点是：它本身是无序的，没法排序。当然
如果我们需求中不需要排序，其实基本可以满足需求。

近期有一个新的 id，[ulid spec](https://github.com/ulid/spec)。这种不仅可以保证基本不重复，而且它
还可以直接进行排序。

我在项目中使用的是 ulid-py


```python
import ulid

uid = ulid.new()
```

## 和日志模块合并

我们在创建 `logger` 时可以使用自定义的 `Formatter`


```python
import contextvars
import logging
import sys

ulid = contextvars.ContextVar("ulid")
logger_name = "awesome-app"
default_formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s][%(ulid)s] %(message)s"
)

stream_handler = logging.StreamHandler(stream=sys.stderr)
stream_handler.setLevel("INFO")
stream_handler.setFormatter(default_formatter)

logger = logging.getLogger(logger_name)
logger.setLevel("INFO")
logger.propagate = False

logger.addHandler(stream_handler)


class UlidFilter(logging.Filter):
    def filter(self, record):
        record.ulid = ulid.get("System")
        return True


ulid_filter = UlidFilter()
for handler in logger.handlers:
    handler.addFilter(ulid_filter)
```

上述代码引入了新的库 `contextvars`。Python 3.7 之后是系统库，之前的需要自己安装下。contextvars
的好处是它和 `async` 是兼容的。在大量异步请求时，上下文可以来回切换，这个值也会发生变化。


## 具体案例

我们使用 Tornado 来实现服务。上述代码保存为 **log.py**。

```python
import ulid
from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop

from log import logger
from log import ulid as uid


class Handler(RequestHandler):

    def prepare(self):
        uid.set(ulid.new())

    async def get(self):
        logger.info("Handle request")


def main():
    url_specs = [("/", Handler)]
    app = Application(url_specs)
    port = 8000
    app.listen(port)
    logger.info(f"Listen on port: {port}")
    for spec in url_specs:
        logger.info(f"{spec[0]}, handler: {spec[1].__class__.__name__}")
    IOLoop.current().start()


if __name__ == "__main__":
    main()

```

可以使用：

```bash
curl http://localhost:8000
```

```python
import threading
import requests

def fun():
    for _ in range(10):
        requests.get("http://localhost:8000")

ts = []
for _ in range(3):
    t = threading.Thread(target=fun)
    t.start()
    ts.append(t)

for t in ts:
    t.join()
```

![Image](/images/python/contextvars-log.png)
