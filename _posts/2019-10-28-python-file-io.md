---
layout: post
title: Python File related IO
categories: [blog, python]
tags: [python]
---

* TOC
{:toc}

### Introduction

Most of the time, we will interact with files or directories on some storage system. Be
familiar with those basic functions will become very handy. This blog is the result of an
internal competition.

### open

The arguments of Python's `open` function is shown below.

```python
open(file,  # path to file
     mode='r',  # mode, "r", "w", "b", "t", "a", "+"
     # 0: turn off buffer (binary), 1: line buffer (text), > 1: bytes, -1: default
     # io.DEFAULT_BUFFER_SIZE
     buffering=-1,
     # file encoding
     encoding=None,
     # encoding & decoding tolerate level
     errors=None,
     # newline indicator
     newline=None,
     # whether `close` called, underlying handler closed at the same time
     closefd=True,
     # user defined opener, returns a file handler
     # called with (file, flags)
     opener=None)
```

Some cases.

```python
path = "test.txt"

fd = open(path, "w")
fd.write("Hell world\n")
# line separator is not added
lines = ["Life is short", "I use python"] * 2
fd.writelines(map(lambda x: x+"\n", lines))
fd.write("Simple is better than complex.\n")
fd.flush()  # flush python buffer to os buffer, os.fsync(fd), force to file
fd.close()

fd = open(path, "r")
data = fd.readline()
print(data)
data = fd.readlines()
print(data)
fd.seek(0, io.SEEK_BEG)
data = fd.read()  # read all, fd.read().splitlines() will strip newline at the end
fd.close()
```

### io module

#### io.StringIO/io.BytesIO

It is similar to C++'s `istringstream` and `ostringstream`. It turns a string or a bytes array
into a file like object.

```python
import io
fd = io.StringIO("hell\nworld\n")
data1 = fd.readline()
data2 = fd.readline()
print(data1)
print(data2)
```

#### io.open

It is the same with `open` function call.


### An interesting example

We want to merge sort two files. In each file, the numbers are sorted.

```python

# content in file1.txt
"""
1
3
5
"""

# content in file2.txt
"""
2
4
8
9
"""

class FileCache(object):
    def __init__(self, fd):
        self._fd = fd
        self._head = None

    def head(self):
        if self._head is None:
            self._head = self._fd.readline().rstrip()
        return self._head

    def next(self):
        self._head = self._fd.readline().rstrip()

with open("file1.txt", "r") as fd1, open("file2.txt", "r") as fd2, open("out.txt", "w") as fd:
    fc1 = FileCache(fd1)
    fc2 = FileCache(fd2)
    while True:
        d1 = fc1.head()
        d2 = fc2.head()
        if d1 == "" and d2 == "":
            break
        if d1 == "":
            fd.write(str(d2)+"\n")
            fc2.next()
            continue
        if d2 == "":
            fd.write(str(d1)+"\n")
            fc1.next()
            continue
        d1 = int(d1)
        d2 = int(d2)
        if d1 > d2:
            fd.write(str(d2)+"\n")
            fc2.next()
        else:
            fd.write(str(d1)+"\n")
            fc1.next()
```

Previous solution is a little tedious.

```python
import heapq
with open("file1.txt", "r") as fd1, open("file2.txt", "r") as fd2, open("out.txt", "w") as fd:
    for data in heapq.merge(fd1, fd2, key=lambda x:int(x)):
        fd.write(data)
```

`heapq` has certain interesting functions:

+ `heapq.push(heap, item)`
+ `heapq.pop(heap)`
+ `heapq.pushpop(heap, item)`
+ `heapq.heapify(heap)`
+ `heapq.heapreplace(heap, item)`: raise `IndexError` if heap is empty.
+ `heapq.merge(*iterables, key=None, reverese=False)`
+ `heapq.nlargest(n, iteraables, key=None)`
+ `heapq.nsmallest(n, iteraables, key=None)`

### Summary

+ If we read the end of a file, `fd.read/fd.readline/fd.readlines` just return an empty string.
`next(fd)` will raise `StopIteration` exception.
  + `read(size=-1)` will return an empty string if it meets `EOF`.
+ `buffering` by default is 8K = `io.DEFAULT_BUFFER_SIZE`
+ `open(path,**)` returns an iterator. We can directly iterate them. `next`, `iter` can be used.
+ For text, `TextIOWrapper`, for binary, `BufferedReader` or `BufferedWriter` is returned from
`open`.

### Reference

+ [Python docs::open](https://docs.python.org/3/library/functions.html?highlight=open#open)
+ [Python docs::io](https://docs.python.org/3/library/io.html)
+ [Python docs:heapq](https://docs.python.org/3/library/heapq.html)
+ [Buffering](https://www.djangospin.com/python-file-buffering/)
