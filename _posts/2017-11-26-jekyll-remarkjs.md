---
layout: post
title: Integrating RemarkJS with Jekyll
categories: [blog, tools]
tags: [tools]
---

[RemarkJS](https://github.com/gnab/remark) 是个非常出色的工具。它能很轻易的 `Markdown` 语法的内容
转换成 PPT。本文想要介绍的是其如何与 Jekyll 结合。

## Remark的简单用法

首先介绍下 `Remark` 的简单用法。

+ PPT 之间的分隔线：`---`, 三个短横线
+ 标题一般是用一个 `#` 的一级标题

举个例子：

```markdown
# Agenda

+ Introduction
+ Topic1
+ Topic2

---

# Introduction

---

# Topic1
```

这样就制作了三页 PPT，第一页是大纲，第二页是 `Introduction`, 第三页是 `Topic1`。

其它的高级用法，请访问 [Remark Wiki](https://github.com/gnab/remark/wiki/Markdown)

## Remark 和 Jekyll 结合

在官方的 [Wiki](https://github.com/gnab/remark/wiki/Using-with-Jekyll) 上有方法说怎么和 `Jekyll`
结合，但是这个方法实际使用起来不行。主要是因为 `Remark` 需要的是 Markdown 文件，而不是被渲染生成
的 HTML 文件。现在 Github 支持的 Jekyll 版本较高，
{%raw%}{{ content  }} 和 {{ page.content }}{%endraw%} 都是
渲染过的。所以现在问题是：

> 如何得到没被渲染过的 Markdown 文件？

首先我们要理解 Jekyll 解析文件的顺序：

+ site 相关变量，page 等
+ Liquid 语法
+ Markdown
+ Layout

在官方 [Wiki](https://github.com/gnab/remark/wiki/Using-with-Jekyll) 中，用户需要新建一个 Layout
的文件，然后在写博客时，将 Layout 指定为对应的 Layout 即可。但是按照上面的顺序，其实 Layout 是最后
解析的，所以在任何时刻，Layout 中看到的都是渲染过的 Markdown 结果。

解决问题的方法：

+ 在对应的 Layout 文件中使用 `include` 语句，{%raw%}{% include {{ slide/page.slide }} %}{%endraw%}
+ 在对应的 post 文件中增加自定义的变量： slide: you-name-it.md

`slide/you-name-it.md` 放在 `_includes` 目录。

最终的方法是：

在对应的 \_posts/ 目录中的文件增加：`slide` 变量

```markdown
---
title: You-name-it
slide: you-name-it.md
---

I like remark
```

在对应的 \_layouts/ 目录中的文件将 `textarea` 中的内容换成：

> {%raw%} {% include {{ page.slide }} %} {%endraw%}

注意前面需要顶格，不要追加额外的空格，否则会打乱 `Remark` 需要的格式。

本文完

