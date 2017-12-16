---
layout: post
title: 如何使用 sphinx 来生成代码文档
tags: [python,]
---

- [注释](#comment)
  - [模块注释](#module-comment)
  - [类的注释](#class-comment)
  - [函数注释](#function-comment)
- [生成文档](#gen-doc)
  - [初始化](#gen-doc-ini)
  - [生成 API 文档](#gen-api-doc)
  - [生成 HTML 文件](#gen-html)
  - [展示网页](#serve-html)

当编写比较大的库时，如果代码具有良好的注释规范，可以使用 `sphinx` 来生成文档。本文主要介绍生成文档
的步骤，以及编写代码中注释的添加方式。本文主要参考 [Reference][1]，更加详细的使用说明可以参考它。
本文主要简单介绍下基本的规范，以及生成文档的方式。

<a name='comment'></a>

### 注释

良好的代码中可能超过 50% 都属于注释。不鼓励写很多不用的注释，但是清晰的注释使得文档的阅读，代码的
理解都会方便很多。个人更加倾向于 [Google 的风格][2]

<a name='module-comment'></a>

#### 模块注释

```python
.. module:: module_name
.. moduleauthor:: some one <some_one@some.com>

# Other documents about `module_name`
```

<a name='class-comment'></a>

#### 类的注释

`>>>` 用于增加代码块，但是注意其前后需要增加空行。

```python

class StarCraft(object):

    StarCraft is a fantastic class.
       Bla. Bla.

       >>> sc = StartCraft()
       >>> sc.start(1, 'north')

    def __init__(self):
        super(StarCraft, self).__init__()

```

<a name='function-comment'></a>

#### 函数的注释

```python
def start(engine, direction):
    start a starcraft
    Args:
       engine(int): engine number
       direction(str, int): direction to fly
    Returns:
       boolean: indicate whether starting operation is successful.
    Raises:
       BadEngineError: engine number is not supported

    pass
```

<a name='gen-doc'></a>

### 生成文档

如果我们是按照上述方式来给模块、类以及函数增加注释的，那么就很容易使用。按照 [参考][1] 中的
`an_example_pypi_project` 的内容来组织代码，其目录结构如下。注意 `usefule_2` 的模块代码不能直接
复制 `useful_1` 的，自己随便增加点内容即可，格式按照上一部分来定。

```shell
an_example_pypi_project
├── __init__.py
├── useful_1.py
└── useful_2.py
```

安装 `sphinx`:

```python
pip install sphinx
```

我们创建任意一个目录，然后 `cd` 进入那个目录。本文在工程同级目录创建了一个 `docs` 目录。

```shell
├── an_example_pypi_project
└── docs
```

<a name='gen-doc-ini'></a>

#### 初始化

然后进入 `docs` 目录，先执行初始化的命令

```shell
sphinx-quickstart
```

有几个选项需要打开：

+ *Separate source and build directories (y/n) [n]:* y
+ *autodoc: automatically insert docstrings from modules (y/n) [n]:* y

此时的目录结构如下：

```shell
├── an_example_pypi_project
├── docs
│   ├── build
│   └── source
│       ├── _static
│       └── _templates
```

<a name='gen-api-doc'></a>

#### 生成 API 文档

第一个选项是指定输出的文件夹，第二个选项是 python 包的路径。

```shell
sphinx-apidoc -o source ../an_example_pypi_project
```

目录结构如下：

```shell
├── Makefile
├── build
└── source
    ├── _static
    ├── _templates
    ├── an_example_pypi_project.rst
    ├── conf.py
    ├── index.rst
    └── modules.rst
```

这个时候有个比较重要的操作，`source/conf.py` 中有部分代码被注释，需要增加回来

```python
import os
import sys
sys.insert(0, os.path.abspath('../..')
# sys.insert(0, os.path.abspath('path-to-an_example_pypi_project')
# 不包括：`an_example_pypi_project`
```

这里的路径是需要执行你模块的所在的目录。

<a name='gen-html'></a>

#### 生成 HTML 文件

进入 `source` 目录, `./html` 是输出的文件夹。

```shell
sphinx-build -b html . ./html
```

如果之前生成过 `Makefile`，在那个 `Makefile` 所在的目录，执行 `make html`，会生成 `build/html/`
目录。

<a name='serve-html'></a>

### 展示网页

到这里，HTML 已经生成，可以展示给用户。使用 `Python` 自带的模块就可以提供服务了。

进入生成的 HTML 文件夹：

```python
python -m SimpleHTTPServer 8080
```

在浏览器中输入 `localhost:8080` 就可以看到之前的代码注释啦~

[1]: https://pythonhosted.org/an_example_pypi_project/sphinx.html
[2]: http://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/

