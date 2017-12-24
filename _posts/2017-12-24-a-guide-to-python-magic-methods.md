---
layout: post
titile: A guide to Python's Magic Methods
category: [python,]
---

翻译自：[A guide to Python's Magic Methods][1]

- 引言[#introduction]
- 构造和初始化[#ctor-and-ini]

<a name='introduction'></a>

### 引言

这篇指导是几个月博客的累积成果，主题是：魔法方法（`magic methods`）。

什么是魔法方法？他们是 Python 面向对象编程的全部，是你为给类增加魔力而添加的特殊方法。魔法方法前后总
是包围着两个下划线(例如，`__init__`, `__lt__`), 而且关于魔法方法的文档不多。所有的魔法方法出现在
Python 文档的同样部分，但是他们到处都有，组织得比较松散。在那部分很难找到一个例子（而且可能那是有意
设计成那样，因为他们会在语言参考中详细描述，伴随着无聊的语法描述等）。

所以，为了解决我认为是 Python 文旦的一个缺陷，我决定为 Python 的魔法方法提供一些用普通英语描述，
例子驱动的文档。我从每周的博客开始，现在已经完成所有的文档，在这篇指引中汇总所有的博客。

希望你会喜欢它。把它作为一个辅助工具，一个温故知新的工具或者一个参考。它只是想成为 Python 魔法方法的
一个用户友好的指导。

<a name='ctor-and-ini'></a>
### 构造和初始化

每个人都知道最基本的魔法方法：`__init__`。这是我们定义一个对象初始化行为的方式。然而当我们调用
`x = SomeClass()` 时，`__init__` 并不是第一个被调用的函数。实施上，第一个被调用的是 `__new__`，由
它来实际创建实例，然后将创建时的参数传递给初始化方法。在对象声明周期的另外一端，有个 `__del__` 函数。
让我们进一步看看这三个函数：

+ `__new__(cls,[...])`
  `__new__` 是在类实例化时第一个被调用的方法。它参数是类，然后是其它要传给 `__init__` 函数的参数。
`__new__` 很少使用，但是它有意义，特别是派生自一个不可变类型，例如 `tupel` 或者 `str`。关于 `__new__`
我不想深入过多细节，因为他们不常用，但是在 [Python 文档][2] 中有详细描述。
+ `__init__(self, [...])`
  类的初始化器。它会被传入任何构造函数调用时的参数（例如，如果我们调用 `x = SomeClass(10, 'foo')`，
`__init__` 会传入 `10` 和 `'foo'` 作为参数），`__init__` 在 Python 类的定义中使用非常广泛。
+ `__del__(self)`
  如果 `__new__` 和 `__init__` 组成了对象的构造函数，那么 `__del__` 就是析构函数。它不是实现语句
`del x` 的行为（这个代码不会翻译成 `x.__del__()`）。相反，它定义的是对象在垃圾回收时的行为。这个在
对象在删除时需要额外清理工作时十分有用，例如套接字或者文件句柄对象。但是请注意，在解释器退出，而
对象还存活时，不保证 `__del__` 一定会执行，所以 `__del__` 不能作为优秀代码实践的替代（例如总是在
使用连接结束时关闭它）。事实上，`__del__` 完全不应该在这种场景下用，因为它不确定的调用情况。谨慎使用。

将上面函数放在一起，下面是一个在实际中使用 `__init__` 和 `__del__` 的例子。

译者注：实际中应该使用 `with` 语句，或者 `contextmanager`

```python
from os.path import join
class FileObject(object):
    '''Wrapper for file objects to make sure the file get closed on deletion.'''

    def __init__(self, filepath='~', filename='sample.txt'):
         # open a file filename in filepath in read and write mode
        self.file = open(join(filepath, filename), 'r+')

    def __del__(self):
        self.file.close()
        del self.file
```

**未完待续**

[1]: https://rszalski.github.io/magicmethods/
[2]: http://www.python.org/download/releases/2.2/descrintro/#__new__
