---
layout: post
title: Python tempfile module
categories: [blog, python]
tags: [python]
---

在开发的过程中，我们时常需要创建一些临时目录或者临时文件来保存一些状态。在 `python` 中一般
会使用 `tempfile` 这个模块。之前其实一直都是利用它的 `gettempdir` 来获取一个临时目录，然后在
临时目录中创建文件，最后在清理掉。实际上 `tempfile` 可以更加的智能。

+ toc
{:toc}

## gettempdir

如果我们的需求是创建一个临时目录，然后最终手动清理掉，则可以使用它。

```python
import subprocess
import tempfile
import uuid

tempdir = tempfile.gettempdir()
file_name = str(uuid.uuid4())
with open(file_name "w") as writer:
    writer.write("hello\nworld\n")

subprocess.call(f"rm -rf {tempdir}", shell=True)
```

上述代码就是在临时目录下随机生成一个文件写入，然后最后再将整个目录删除。


## TemporaryFile

这个是生成一个临时的文件(并不一定真的生成文件)，当它 `close` 时，文件会被自动清理。
它返回的是 `file-like` 对象。根据我们创建时的 `mode`，我们可以操作它，它没有名字。

```python
import tempfile

file = tempfile.TemporaryFile("w+")

file.write("hello\nworld\n")
file.flush()

file.seek(0)
print(file.read())

```

## NamedTemporaryFile

相对于 `TemporaryFile`，它会真实地去创建一个文件。你可以利用它的名字来找到具体的文件地址，
重新打开，然后读取其内容，而不必 `seek(0)` 来实现重新读取。

```python
import tempfile

file = tempfile.NamedTemporaryFile("w+")

file.write("hello\nworld\n")
print(f"{file.name}")
file.flush()

file.seek(0)
print(file.read())

with open(file.name) as reader:
    print(reader.read())
```

## TemporaryDirectory

和 `NamedTemporaryFile` 类似，它是返回一个有名字的目录。我们可以在目录任意创建文件，
当退出时，会被清理。

```python
import os
import tempfile

with tempfile.TemporaryDirectory() as directory:
    path = os.path.join(directory, "a.txt")
    with open(path, "w") as writer:
        writer.write("hello\nworld\n")
    with open(path) as reader:
        print(reader.read())
```

## 总结

上述 3 个都可以用成 `context`，即 `with` 的语法。当 `context` 退出时，文件就自动被清理。
相对于自己创建，然后删除比较灵活。缺点是如果原来代码就很多缩进，再加一层可能会比较难看。
如果是这样，那就应该重构代码了。

## Reference

+ [tempfile](https://docs.python.org/3/library/tempfile.html#tempfile-examples)
