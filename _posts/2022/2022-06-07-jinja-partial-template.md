---
layout: post
title: Partially render in Jinja
categories: [blog, python]
tags: [python]
---


A Jinja template can be rendered. Sometimes the data we need can not be collected in
just one place. It will be helpful if we can render a template multiple times.

+ toc
{:toc}

By default, a Jinja template can not be rendered multiple times. It will raise an
exception or insert null values into the corresponding placeholders.

In the blog, we will use a trick to mimic the partially rendering behavior. Jinja has an
operator `raw` which can be used to render its original content.

{% raw %}

```python
from jinja2 import Template
template_str = """
{% raw %}{%{% endraw %} raw {% raw %}%}{% endraw %}
{{hi}}
{% raw %}{%{% endraw %} endraw {% raw %}%}{% endraw %}
"""

partial_template_str = Template(template_str).render()

result = Template(partial_template_str).render(hi=3)

```

But using `raw` will introduce redundant newlines. We can not use `-` to remove the spaces.
It is wrong sometimes we remove the leading spaces.

```python
from jinja2 import Template
template_str = """
{% raw %}{%{% endraw %} raw {% raw %}%}{% endraw %}
{{hi}}
{% raw %}{%{% endraw %} endraw {% raw %}%}{% endraw %}
"""

partial_template_str = Template(template_str, trim_blocks=True, lstrip_blocks=True).render()

result = Template(partial_template_str).render(hi=3)
print(result)

```

If the leading spaces are not meaningless to your program, you can use `-`
to remove them. [Referecne](https://jinja.palletsprojects.com/en/3.1.x/templates/#escaping)

```python
from jinja2 import Template
template_str = """
{% raw %}{%{% endraw %} raw {% raw %}-%}{% endraw %}
{{hi}}
{% raw %}{%{% endraw %} endraw {% raw %}%}{% endraw %}
"""

partial_template_str = Template(template_str, trim_blocks=True, lstrip_blocks=True).render()

result = Template(partial_template_str).render(hi=3)
print(result)

```

If we need more nested templates, such as we want a template to be rendered three
or more times, the code will be ugly. It seems that Jinja does not provide way to
implement a customized operator


```python
from jinja2 import Template
template_str = """
{% raw %}{%{% endraw %} raw {% raw %}-%}{% endraw %}
{{hi}}
{% raw %}{%{% endraw %} endraw {% raw %}-%}{% endraw %}

{% raw %}
{{'{%'}} raw {{'%}'}}
{% endraw %}
{% raw %}
{{hello}}
{% endraw %}
{% raw %}
{{'{%'}} endraw {{'%}'}}
{% endraw %}

"""

partial_template_str = Template(template_str, trim_blocks=True, lstrip_blocks=True).render()
print(partial_template_str)
print("=" * 10)

result = Template(partial_template_str).render(hi=3)
print(result)
print("=" * 10)

final_result = Template(result).render(hello=4)
print(final_result)
```

`raw` and `endraw` can not be nested. You are not allowed to insert `raw` and
`endraw` block in another `raw` and `endraw` block`.
