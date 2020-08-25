---
layout: post
title: Python unittest and unittest.mock
categories: [blog, python]
tags: [python]
---

Each language has its own known testing framework which makes writing test cases easier. In
Python, the standard and built-in are `unittest` module. Together with `pytest` or `coverage`,
we can get a statistics of all the tests which can be displayed in GUI.

+ toc
{:toc}

### test cases in unittest

+ Implement a class which inherits from `unittest.TestCase`
+ Add tests
  + Call related `assert*` methods to check results
+ Add an entrance for the testing module

```python
import operator
import unittest


class SimpleTestCase(unittest.TestCase):

    def test_add(self):
        a = 2
        b = 3
        self.assertEqual(5, operator.add(2, 3))


if __name__ == "__main__":
    unittest.main()
```

#### Running the test

We have added `__name__` related code, so we can directly call the module. Assuming previous
code is saved in a file named `simple_test.py`, we can run:

```bash
# Run all the tests in the module
python -m unittest simple_test[.py]

# Run a single test
python -m unittest simple_test.SimpleTestCase.test_add
```

If `simple_test.py` is saved in a different folder which means in a different module, we need
to make sure that the testing module is importable. If `simple_test` is saved under a folder
named `tests`, then there should be a `__init__.py` under that.

```python
python -m unittest tests/simple_test.py
```

#### Before and after a test

If there are codes we need to run before a test (initialization code) or after a test (cleanup
code), we can override `setUp` and `tearDown`.

```python
import operator
import unittest

class SQLDB(object):

    def connect_db(self):
        pass

    def read_record(self):
        return 1

    def disconnect_db(self):
        pass


class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        self._db = SQLDB()
        self._db.connect_db()

    def tearDown(self):
        self._db.disconnect_db()

    def test_add(self):
        self.assertEqual(1, self._db.read_record())


if __name__ == "__main__":
    unittest.main()
```

#### Skip certain tests

If there are tests we want to skip under certain condition, we can skip it instead of emitting
an error by running it. We can skip a whole test and any single test by decorating with
`unittest.skipIf`

```python
import operator
import os
import unittest

try:
    import SQLDB
except ModuleNotFoundError:
    SQLDB = None

class SQLDB(object):

    def connect_db(self):
        pass

    def read_record(self):
        return 1

    def disconnect_db(self):
        pass


@unittest.skipIf(SQLDB is None, "SQLDB is not available")
class SimpleTestCase(unittest.TestCase):

    def setUp(self):
        self._db = SQLDB()
        self._db.connect_db()

    def tearDown(self):
        self._db.disconnect_db()

    @unittest.skipIf("DB_TEST" not in os.environ, "Not a testing environment")
    def test_add(self):
        self.assertEqual(1, self._db.read_record())


if __name__ == "__main__":
    unittest.main()
```

There are other skipping decorators:

+ `skip(reason)`
  + Used to write customized skipping decorators

```python
# Refer to https://www.chunyangwen.com/blog/python/python-descriptor-decorator.html
# for more details about a decorator

def skipUnlessHasattr(obj, attr):
    if hasattr(obj, attr):
        return lambda func: func
    return unittest.skip("{!r} doesn't have {!r}".format(obj, attr))
```

+ `skipUnless(condition, reason)`
+ `skipIf(condition, reason)`
+ `unittest.expectedFailure`: A failure is a success.

#### Asserting methods

|----|----|
|Method|Checks that|
|assertEqual(a, b)| a == b|
|assertNotEqual(a, b)| a != b|
|assertTrue(x)|bool(x) is True|
|assertFalse(x)|bool(x) is False|
|assertIs(a, b)|a is b|
|assertIsNot(a, b) | a is not b|
|assertIsNone(a) | a is None|
|assertIsNotNone(a)| a is not None|
|assertIn(a, b) | a in b|
|assertNotIn(a, b)| a not in b|
|assertIsInstance(a, b)|isinstance(a, b)|
|assertNotIsInstance(a, b)|not instance(a, b)|
|Raises or warnings|
|assertRaises(exc, fun, \*args, \*\*kwargs) |fun(\*args, \*\*kwargs) raise exc|
|assertRaisesRegex(exc, r, fun, \*args, \*\*kwargs) |fun(\*args, \*\*kwargs) raise exc, message matches regex r|
|assertWarns(warn, fun, \*args, \*\*kwargs) |fun(\*args, \*\*kwargs) raise exc|
|assertWarnsRegex(warn, r, fun, \*args, \*\*kwargs) |fun(\*args, \*\*kwargs) raise warn, message matches regex r|
|assertLogs(logger, level)|The with block logs on logger with minimum level|
|Number related|
|assertAlmostEqual(a, b)|round(a-b, 7) == 0|
|assertNotAlmostEqual(a, b)|round(a-b, 7) != 0|
|assertGreater(a, b)|a > b|
|assertGreaterEqual(a, b) |a >= b|
|assertLess(a, b)|a < b|
|assertLessEqual(a, b)|a <= b|
|assertRegex(s, r)|r.search(s)|
|assertNotRegex(s, r)|not r.search(s)|
|assertCountEqual(a, b)|a and b have the same elements in the same number, regardless of the order|
|Sequence related|
|assertMultLineEqual(a, b)|strings|
|assertSequenceEqual(a, b)|sequences|
|assertListEqual(a, b)|lists|
|assertTupleEqual(a, b)|tuples|
|assertSetEqual(a, b)|sets or frozensets|
|assertDictEqual(a, b)|dicts|

#### Common practices

```python
# assert whether certain log happens
with self.assertLogs(logger, level="INFO") as cm:
    # bla bla
    self.assertRegex(" ".join(cm.output), ".*xxx.*")
```

```python
with self.assertRaises(ValueError):
    # bla bla
```

### unittest.mock

Mock is very important is tests.

+ You don't want your test cases fail due to an unrelated service.
+ You don't want your test cases coupled with each other:
  + Testing functionalities of `a` while `b` may fail.

#### A simple case

Usually we will use `unittest.mock.patch` to help us write tests. We can patch:

+ constants
  + Actually I think this is easy done without `mock`.
+ a module function
+ a class method
+ a static method
+ an object method

```python
# my_module.py

import os

def get_more_magic_values():
    return [42] * 2


def get_magic_value():
    return get_more_magic_values()[0]


def listdir(p):
    return os.listdir(p)


class ObjectToBeMocked(object):

    HelloWorld = 3

    def hello(self):
        return ObjectToBeMocked.HelloWorld

    def hi(self):
        return self.hello() + 1

    @property
    def beer(self):
        return -1

    @classmethod
    def oops(cls):
        return "oops"
```

We save above code into a file named `my_module.py`. Most of the functions and methods
are just naively implemented. So how we can test it?

```python
import unittest
from unittest import mock
from unittest.mock import patch
from my_module import ObjectToBeMocked
import my_module


class MyModuleTest(unittest.TestCase):

    @patch("my_module.ObjectToBeMocked.HelloWorld", 42)
    def test_hello(self):
        self.assertEqual(42, my_module.ObjectToBeMocked().hello())

    @patch.object(my_module.ObjectToBeMocked, "hello", return_value=42)
    def test_hi(self, hello):
        o = ObjectToBeMocked()
        self.assertEqual(43, o.hi())

    @patch.object(my_module.ObjectToBeMocked, "hello")
    def test_hi_1(self, hello):
        hello.return_value = -1
        o = ObjectToBeMocked()
        self.assertEqual(0, o.hi())

    @patch("my_module.get_more_magic_values")
    def test_get_magic_value(self, get_more_magic_values):
        get_more_magic_values.return_value = [41]
        self.assertEqual(41, my_module.get_magic_value())

    @patch("my_module.ObjectToBeMocked.beer", new_callable=mock.PropertyMock())
    def test_property_beer(self, prop):
        prop.return_value = -2
        self.assertEqual(-2, my_module.ObjectToBeMocked().beer())

    @patch("my_module.os")
    def test_mock_os(self, mock_os):
        mock_os.listdir.return_value = ["hi", "hello"]
        self.assertListEqual(["hi", "hello"], my_module.listdir("."))

```

#### Notes

+ We have to mock the module where it is used. **NOT** from a general place
  + Please refer to `mock_os`
+ When it comes to an instance, `patch.object` is used instead of `patch`.
+ Difference between `patch` and `patch.object`:
  + `patch.object` mocks a single method or attributes, target is also the class

#### classes

+ `unittest.mock.Mock`
+ `unittest.mock.MagicMock`
+ `unittest.mock.PropertyMock`
+ `unittest.mock.AsyncMock`

#### Common practices

```python
# create a side-effect
with patch(Clz, "method", side_effect=ValueError) as mock_method:
    ins = Clz()
    self.assertRaise(ValueError):
        ins.method()
```

```python

from unittest.mock import create_autospec

# automatically behaves like `Clz`
MockObject = create_autospec(Clz)
```


### Reference

+ [Python unittest](https://docs.python.org/3/library/unittest.html)
+ [Python unitest.mock](https://docs.python.org/3/library/unittest.mock.html)
+ [unittest.mock cookbook](https://chase-seibert.github.io/blog/2015/06/25/python-mocking-cookbook.html)
+ [Real Python](https://realpython.com/python-mock-library/#patching-an-objects-attributes)
