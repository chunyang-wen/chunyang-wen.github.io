---
layout: post
title: logger.debug cause performance issue
categories: [blog, python]
tags: [python]
---

A logger is preferred in a formal project, because we can set different levels
for different loggers, redirect log messages to files (even to remote servers), specify
a unified format for logs and etc.

+ toc
{:toc}

Recently I am using [py-spy](https://github.com/benfred/py-spy) to create a flame
graph for my program in order to find out which part is slow.

```bash
py-spy record -o profile.svg -- python a.py
```

After generating `profile.svg` and view it using a browser, I found that there are a
lot of `arrayprint` clauses from numpy package. The clauses are similar  as following:

```python
array = np.array([1,2,3,])
logger.debug(f"Array: {array}")
```

I have added a bunch of debug codes to help me find problems during the
developing stage. To me, it should not cause any performance problem if the log
level is higher than `DEBUG`.

After reading the code, it is obvious that, use `f-str` does not help here.
`f-str` is the message, it is the log record itself.

![Log flow](/images/python/logging_flow.png)

[Link](https://docs.python.org/3/howto/logging.html#logging-flow). By default,
no `LogRecord` is created if the corresponding level is not enabled.
A `LogRecord` is created using string formatting.

```python
def getMessage(self):
    """
    Return the message for this LogRecord.

    Return the message for this LogRecord after merging any user-supplied
    arguments with the message.
    """
    msg = str(self.msg)
    if self.args:
        msg = msg % self.args
    return msg
```

if We change the log related code as following:

```python
logger.debug("Array: %s", array)
```

There will be no `LogRecord` created, no `arrayprint` from numpy code will be called.


Have fun!
