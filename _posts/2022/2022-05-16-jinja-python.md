---
layout: post
title: Python Jinja2
categories: [blog, python]
tags: [python]
---


[Jinja2](https://jinja.palletsprojects.com/en/3.1.x/) is a fast, expressive,
extensible templating engine. This blog records the problems or requirements I met
during my development.

+ toc
{:toc}


## Basic usage

+ `{{...}}` for expressions
+ `{% ... %}` for statements
+ `{# ... #}` for comments

Jinja2 placeholders are wrapped with double curly braces.

### Use strings as templates

```python
from jinja2 import Template

content = "{{apple_cnt}}"
template = Template(content)

result = template.render(apple_cnt=3)
print(result)
```

### Use a folder as templates sources

```python
from jinja2 import Envrionment, PackageLoader

env = Environment(
    loader=PackageLoader("package_name", "path/to/templates"),
)
template = env.get_template("a.html")
```

We may package templates with our published packages, using `package_data` in setup.py.
[Reference](https://www.chunyangwen.com/blog/python/python-setup.html#package_data)

```python
from jinja2 import Envrionment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader(["/path/to/A"])
)
template = env.get_template("a.html")
```

Get templates for a folder from file system.

## Advanced usage

### Comment

```yaml
{# This is a comment #}
```

### Raise error if certain key not found

```python
from jinja2 import Envrionment, FileSystemLoader

def raise_helper(msg):
    raise Exception(msg)

env = Environment(
    loader=FileSystemLoader(["/path/to/A"])
)

env.globals["raise"] = raise_helper

template = env.get_template("a.html")
```

We can add following template code, calling our predefined `raise_helper`

```yaml
{% if app_name is none or app_name|length < 1 %}
{{ raise("app_name must be set") }}
{% endif %}
```

### Dict related variable

`env` is a dict.

```yaml
{% for key, value in env.items() %}
{% endfor %}

A: env["HOST_IP"]
{% if "HOSTNAME" in env %}
B: env["HOSTNAME"]
{% else %}
B: "UNKNOWN"
{% endif %}
```

`is mapping` is a test.

[Jinja2 tests](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-tests)

+ `mapping`
+ `sequence`
+ `string`
+ `integer`
+ `float`
+ `callable`
+ `iterable`

### Trim empty spaces and blocks

By default `{% else %}` or similar expression will be empty blocks after render.

```python
from jinja2 import Environment, Template
template = "{{apple_cnt}}"
Template(template, trim_blocks=True, lstrip_blocks=True)

env = Environment(
    loader=PackageLoader("package_name", "path/to/templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)
```

### Default value

```yaml
{{replicas|default(1, true)}}
```

[default](https://jinja.palletsprojects.com/en/3.1.x/templates/?highlight=default%20function#jinja-filters.default)

The second bool is required if the variable may be evaluated to `false` which means `false`
is a valid value.

[Jinja2 filters](https://jinja.palletsprojects.com/en/3.1.x/templates/#builtin-filters)

### autoescape

[Autoescape](https://jinja.palletsprojects.com/en/3.1.x/api/#autoescaping)

Keep double quotation in string, not escaped.

```python
from jinja2 import Template, select_autoescape

t = """
{% autoescape false %}
b: {{cnt}}
{% endautoescape %}
"""

template = Template(t)

result = template.render(cnt='"3"')
print(result)
```

If we set `false` to `true` for `autoescape`, we will get

```python
b: &#34;3&#34;
```

```python
from jinja2 import Template
from jinja2.utils import select_autoescape

t = """
b: {{cnt}}
"""

template = Template(t, autoescape=select_autoescape(default_for_string=False))

result = template.render(cnt='"3"')
print(result)
```

### Create variables

```yaml
{% set a = 3 %}
```

## Reference

+ [Template designer documentation](https://jinja.palletsprojects.com/en/3.1.x/templates/)
+ [Source code](https://github.com/pallets/jinja)
