---
layout: post
title: Build tensorflow on Mac
categories: [blog, tensorflow]
tags: [tensorflow]
---

Building tensorflow from source on mac is really not an easy thing at first.
This blog introduces problems met during building.

+ toc
{:toc}

### Bazel installation

On mac, you can install lots of command line tools using [Homebrew](https://brew.sh/).

```bash
brew install bazel
```

It is a pity that I cannot specify the version like `brew install bazel@0.21.0`.

Why I want to install version 0.21.0? Please refer to [Github issue](https://github.com/tensorflow/tensorflow/issues/30556).
Different versions of tensorflow has different requirements. Currently I am building **r1.13**.
It requires bazel with a version lower than 0.21.0.

Go to [Github bazel release page](https://github.com/bazelbuild/bazel/releases), find the version
you need and download it. BTW, (releases/tag/${version}) will directly go to the corresponding
page.

### Build command

#### Configure

```bash
./configure
```

Select functions you care and you are ready to go.

#### Build

```bash
bazel build -c opt //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

The first command sometimes fails with no reasons, you just keep retry it (Oops!).

The second command will generate the wheel file you need to install.

#### @org_python_license

The checksum is not correct. Just modify the file in `tensorflow/tensorflow/workspace.bzl` and
change the sha1 value in `sha256_urls`.

[Reference in Chinese](https://zhuanlan.zhihu.com/p/121630894)

#### Generate package

**google/protobuf/port_def.inc** not found. [Github issue](https://github.com/tensorflow/tensorflow/issues/27697)

It seems that tensorflow misses files. Way to fix [Commit](https://github.com/testkevinbonz/tensorflow/commit/2cca49f1bb6fbfae6df658e61097608047f0900a)

### Run tensorflow

A annoying warning:

```python
>>> import tensorflow
/Users/chunyangwen/Documents/envs/python3.7.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:526: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint8 = np.dtype([("qint8", np.int8, 1)])
/Users/chunyangwen/Documents/envs/python3.7.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:527: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_quint8 = np.dtype([("quint8", np.uint8, 1)])
/Users/chunyangwen/Documents/envs/python3.7.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:528: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint16 = np.dtype([("qint16", np.int16, 1)])
/Users/chunyangwen/Documents/envs/python3.7.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:529: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_quint16 = np.dtype([("quint16", np.uint16, 1)])
/Users/chunyangwen/Documents/envs/python3.7.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:530: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  _np_qint32 = np.dtype([("qint32", np.int32, 1)])
/Users/chunyangwen/Documents/envs/python3.7.7/lib/python3.7/site-packages/tensorflow/python/framework/dtypes.py:535: FutureWarning: Passing (type, 1) or '1type' as a synonym of type is deprecated; in a future version of numpy, it will be understood as (type, (1,)) / '(1,)type'.
  np_resource = np.dtype([("resource", np.ubyte, 1)])
```

Please change the file `tensorflow/python/framework/dtypes.py`. Replace the number from 526 to
535 with a pair of parentheses and a comma.

```python
# before
_np_qint8 = np.dtype([("qint8", np.int8, 1)])
# after
_np_qint8 = np.dtype([("qint8", np.int8, (1,))])
```

Have fun!
