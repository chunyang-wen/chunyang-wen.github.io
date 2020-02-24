---
layout: post
title: setup.py in Python
categories: [blog, python]
tags: [python]
---

When we create a python package, we will distribute it. There are a couple of ways to
achieve this purpose:

+ by source code
+ by whl
+ by uploading it to pypi

The last two methods require us to write a `setup.py` to build the package.

* TOC
{:toc}

### Introduction

After finishing reading this blog, you are good to write a `setup.py` which behaves
well in most cases.

Let's create a simple package using `setup.py`.

```bash
├── awesome
│   ├── __init__.py
│   ├── __main__.py
│   └── data
│       └── data.txt
└── setup.py
```

The content of the files:

```python
# __init__.py
__version__ = "0.0.1"
```

```python
# __main__
#!/usr/bin/env python
# coding: utf-8


def main():
    print("Hello awesome boy")


if __name__ == "__main__":
    main()
```

```python
# setup.py
#!/usr/bin/env python
# coding: utf-8

from setuptools import find_packages, setup

import awesome

install_requires = ["wheel"]

extras_require = {
    "np": ["numpy"]
}


def install():
    setup(
        name="awesome",
        version=awesome.__version__,
        description="awesome package",
        author="Some awesome team",
        packages=find_packages(where=".", exclude=["ghost"]),
        install_requires=install_requires,
        extras_require=extras_require,
        package_data={"awesome": ["data/data.txt"]},
        entry_points={
            "console_scripts": ["awesome = awesome.__main__:main"]
        },
    )


install()
```

### Build an install

```bash
python setup.py bdist_wheel
cd dist && pip install *.whl && cd -
```

The first command will generate corresponding `*.whl` files under dist directory. We can
distribute the wheel file or upload it to any pypi server.

### Analysis of setup.py

The entrance is the `setup` function. It has a couple of arguments we are interested in.

#### name, version, description, author

These fields are the common information of your package. Usually we put information in
package's `__init__.py` and read from there instead of hard coding them here.

#### packages

Instruct `setup` function to find your packages.

```python
find_packages(where='.', exclude=(), include=('*',))
    """Return a list all Python packages found within directory 'where'

    'where' is the root directory which will be searched for packages.  It
    should be supplied as a "cross-platform" (i.e. URL-style) path; it will
    be converted to the appropriate local path syntax.

    'exclude' is a sequence of package names to exclude; '*' can be used
    as a wildcard in the names, such that 'foo.*' will exclude all
    subpackages of 'foo' (but not 'foo' itself).

    'include' is a sequence of package names to include.  If it's
    specified, only the named packages will be included.  If it's not
    specified, all found packages will be included.  'include' can contain
    shell style wildcard patterns just like 'exclude'.
    """
```

#### install_requires

This describes the requirements of your package. Valid forms are:

+ numpy
+ numpy==1.0.0

#### extra_require

This is optional. The type is a dict, keys are the extra requirement names, values are similar
forms to `install_requires`. It is used to easily support different extensions without
installing everything at the same time.

```shell
pip install awesome-0.0.1-py3-none-any.whl\[np\]  # in zsh, to escape

numpy; extra == "np" in /xx/lib/python3.6/site-packages (from awesome==0.0.1) (1.16.4)
```

#### package_data

We can package additional data with our package. After adding them, how can we retrieve them?

```python
import pkg_resources
path = pkg_resources.resource_filename("awesome", "data/data.txt")
```

#### entry_points

`entry_points` is used to execute the package as a shell command. We install the wheel file
genereated in `dist` directory. For example, previous package can be directly executed as
`awesome`. It will print "Hello awesome boy".

```bash
awesome
> Hello awesome boy
```

### Reference

+ <a href="https://docs.python.org/3/distutils/setupscript.html" target="_blank">Python doc</a>
