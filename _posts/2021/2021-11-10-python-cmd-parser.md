---
layout: post
title: Python command line comparison
categories: [blog, python]
tags: [python]
---

编写 Python 的命令行程序时，一个很重要的问题是：如何声明参数，然后解析，最终被程序调用。能否灵活的
声明，组合会决定我们是否需要用额外的代码来替代这些功能。例如参数的互斥，子命令等。

+ toc
{:toc}


## 总结

本次主要对比 `argparse`, `click` 和 `fire`。

- 如果你不想引入额外依赖，使用 `argparse`
- 对于特别简单的应用，建议使用 `click`来编写即可。因为只用加一个 decorator 即可完成所有的事情。
- 对于复杂的应用场景，太多的参数注解会让函数看起来有点奇怪
- `fire` 的应用场景感觉在事后。即开发时并不是想把功能以命令行形式暴露，但是后续想以命令行暴露。
为了避免大量的更改，`fire` 可以快速实现转化。

## argparse

[ArgParse](https://docs.python.org/3/library/argparse.html)

下面代码展示了大部分的功能。全部功能请参数上面链接。

> parse 函数在工作中，个人更偏向于 `parse_known_args`，避免由于用户误传或者多传导致
> 程序整体失败。`parser_args` 可以做更强的校验。

```python
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument(
    "--user",
    default=1,
    type=int,
    help="User to say hello",
)

parser.add_argument(
    "--users",
    action="append",
    help="Users to say hello",
)

parser.add_argument(
    "--verbose0",
    "-v0",
    action="store_true",
    help="Verbose log",
)
# 实际上 action="store_true" 不是在任何情况下都工作的很好
# 下面这段代码
default = False
parser.add_argument(
    "--silent",
    nargs="?",
    const=not default,
    default=default,
    type=lambda x: x.lower() in ["true", "yes", "t", "y"],
    help="Add a bool argument",
)

# Available action
"""
store_action = "store_true", "store_false", "store_const",
# extend 允许 --foo a b c
# append 允许 --foo a --foo b
append_action = "append", "append_const", "extend"
count_action = "count
"""
parser.add_argument(
    "--str", dest="types", action="append_const", const=str
)
parser.add_argument(
    "--verbose", "-v", action='count', default=0
)
# positional argument
parser.add_argument(
    "number",
)

##### subparsers

sub_parsers = parser.add_subparsers(dest="cmd", help="subcomamnd help")
holy_parser = sub_parsers.add_parser(
    "holy", aliases=["hy"], help="holy help"
)
holy_parser.add_argument("--holy")


#### Mutually exclusive group
group = parser.add_mutually_exclusive_group()
group.add_argument("--foo-mu", action="store_true", dest="mu")
group.add_argument("--bar-mu", action="store_true")

# nargs="?", "+", "*", int
# choices 只能在限定范围内选取

args1 = parser.parse_args(args=None) # will use sys.args
args2, unknown_args = parser.parse_known_args(args=None)
```

+ `argparse` 支持 namespace

```python
import argparse

class CommandNamespace(argparse.Namespace):
    pass

command = CommandNamespace()

parser = argparse.ArgumentParser()
parser.add_argument("--world")

args, _ = parser.parse_known_args(namespace=command)

print(args is command)

print(args)
```

+ `argparse` 支持把不能解析的参数放入一个单独变量

```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("remain_args", nargs=argparse.REMAINDER)
```

## click

- [Homepage](https://click.palletsprojects.com/en/8.0.x/quickstart/)
- [Examples](https://github.com/pallets/click/tree/main/examples)

```python
import click


@click.group()
def clickme():
    pass


@clickme.command()
def initdb():
    click.echo('Initialized the database')


@clickme.command()
def dropdb():
    click.echo('Dropped the database')


@click.command()
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def hello(count, name):
    for _ in range(count):
        click.echo(f"Hello {name}!")


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context  # Pass context between nested commands
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug

@cli.command()
@click.pass_context
def sync(ctx):
    click.echo(f"Debug is {'on' if ctx.obj['DEBUG'] else 'off'}")

if __name__ == '__main__':
    cli(obj={})

```

### Types

```python
import click

@click.command()
@click.option("--username", prompt=True)  # hide_input=True to enable password
@click.password_option()
def hi(username):
    click.echo(f"{username}")

click.prompt("Please input your user name", type=int)

if click.confirm("Do you want to continue", abort=True):
    click.echo("Keep firing")
```

### Multi Command

#### Pass context

```python
@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below)
    ctx.ensure_object(dict)

    ctx.obj['DEBUG'] = debug

@cli.command()
@click.pass_context
def sync(ctx):
    click.echo(f"Debug is {'on' if ctx.obj['DEBUG'] else 'off'}")

if __name__ == '__main__':
    cli(obj={})
```

#### Merging

```python
import click

@click.group()
def cli1():
    pass

@cli1.command()
def cmd1():
    """Command on cli1"""

@click.group()
def cli2():
    pass

@cli2.command()
def cmd2():
    """Command on cli2"""

cli = click.CommandCollection(sources=[cli1, cli2])

if __name__ == '__main__':
    cli()

```

#### Chaining

```python
@click.group(chain=True)
def cli():
    pass


@cli.command('sdist')
def sdist():
    click.echo('sdist called')


@cli.command('bdist_wheel')
def bdist_wheel():
    click.echo('bdist_wheel called')
```

#### Pipelines

```python
@click.group(chain=True, invoke_without_command=True)
@click.option('-i', '--input', type=click.File('r'))
def cli(input):
    pass

@cli.result_callback()
def process_pipeline(processors, input):
    iterator = (x.rstrip('\r\n') for x in input)
    for processor in processors:
        iterator = processor(iterator)
    for item in iterator:
        click.echo(item)

@cli.command('uppercase')
def make_uppercase():
    def processor(iterator):
        for line in iterator:
            yield line.upper()
    return processor

@cli.command('lowercase')
def make_lowercase():
    def processor(iterator):
        for line in iterator:
            yield line.lower()
    return processor

@cli.command('strip')
def make_strip():
    def processor(iterator):
        for line in iterator:
            yield line.strip()
    return processor
```

#### pass config

```python
import click


class Config:
    pass

pass_config = click.make_pass_decorator(Config, ensure=True)


@click.group()
@pass_config
def cli(config):
    config.hi = 3


@cli.command()
@click.option("--user")
@pass_config
def hi_times(config, user):
    for _ in range(config.hi):
        click.echo(f"Hi {user}")
```

### Testing

[Testing](https://click.palletsprojects.com/en/8.0.x/testing/)

```python
# hello.py
import click

@click.command()
@click.argument('name')
def hello(name):
   click.echo(f'Hello {name}!')
```
```python
from click.testing import CliRunner
from hello import hello

def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(hello, ['Peter'])
  assert result.exit_code == 0
  assert result.output == 'Hello Peter!\n'


```
### 区别

- option 和 argument 单独区分开
- **argument 不支持 help，argument 可以设置 require = False**
- 测试支持
- command 的组合比较灵活，可以 Chain，可以 Pipeline，可以同时执行
- command 之间可以传递信息，通过 ctx
- 可以自动支持 File，而且是 lazy，是只有在真实 IO 时才会写出
   - click.File("w")

## fire

[Guide](https://github.com/google/python-fire/blob/master/docs/guide.md)

自动将任何 Python 程序自动组装成命令行接口

### fire anything

```python
import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire()
```

- add 和 multiply 是 command 的名字
```bash
python hello.py add 10 20
python hello.py multiply 10 20
```

### fire a function

```python
import fire

def hello(name):
  return 'Hello {name}!'.format(name=name)

if __name__ == '__main__':
  fire.Fire(hello)
```

```bash
python hello.py John
```

### fire a dict

```python
import fire

def add(x, y):
  return x + y

def multiply(x, y):
  return x * y

if __name__ == '__main__':
  fire.Fire({
      'add': add,
      'multiply': multiply,
  })
```

### fire an object

```python
import fire

class Calculator(object):

  def add(self, x, y):
    return x + y

  def multiply(self, x, y):
    return x * y

if __name__ == '__main__':
  calculator = Calculator()
  fire.Fire(calculator)
```

### fire a class

```python
import fire

class BrokenCalculator(object):

  def __init__(self, offset=1):
      self._offset = offset

  def add(self, x, y):
    return x + y + self._offset

  def multiply(self, x, y):
    return x * y + self._offset

if __name__ == '__main__':
  fire.Fire(BrokenCalculator)
```

```bash
python hello.py add 10 10 --offset 0
```

Fire 建议使用 class，可以在 fire 时，为 class 提供构造函数参数。

### grouping commands

```python
class IngestionStage(object):

  def run(self):
    return 'Ingesting! Nom nom nom...'

class DigestionStage(object):

  def run(self, volume=1):
    return ' '.join(['Burp!'] * volume)

  def status(self):
    return 'Satiated.'

class Pipeline(object):

  def __init__(self):
    self.ingestion = IngestionStage()
    self.digestion = DigestionStage()

  def run(self):
    self.ingestion.run()
    self.digestion.run()
    return 'Pipeline complete'

if __name__ == '__main__':
  fire.Fire(Pipeline)
```

```bash
$ python example.py run
Ingesting! Nom nom nom...
Burp!
$ python example.py ingestion run
Ingesting! Nom nom nom...
$ python example.py digestion run
Burp!
$ python example.py digestion status
Satiated.
```

### fire by a command line

```python
def hello(name):
  return 'Hello {name}!'.format(name=name)
```

```bash
# .py is optional if hello is reachable as a module
python -m fire hello[.py] hello --name="John"
```

### 区别

- 本身不是为了制造命令行工具，而是方便将任何 Python 组件以命令行形式暴露出去，不用编写复杂的参数声明和解析。使用场景下不太一致
- 自动支持 bool
   - --flag=True
   - --noflag
- 支持 dict 参数解析
   - `python example.py --d '{"name": "Justin"}'`
