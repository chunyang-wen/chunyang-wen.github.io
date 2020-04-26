---
layout: post
title: why indentLint not working with mac vim (8.0)?
categories: [blog, tools]
tags: [tools]
---

+ [问题](#problem)
+ [解决方法](#solution)
+ [Backspace 失效](#bp-not-working)

之前有一次误操作，将 `~` 文件夹进行了删除。幸亏及时遇到了权限问题，没有清理完，不然要悲剧。现在已经
将 `rm` 重定向成 `mv` 操作。

```bash
alias rm="mv $@ ~/.trash"
```
<a id = "problem"></a>

### 问题

虽说这次删除并没有删除干净，但是也破坏了我一些工具，其中比较重要的是 `vim`。之前在 `Github` 上备份
过插件，直接 `clone` 下来就好。在重装之余，想额外安装一个插件：
[indentLine](https://github.com/Yggdroot/indentLine)

安装的原因是 `Python` 代码。

插件管理方式使用的：`Pathogen`。所以只要将这个仓库克隆到 `~/.vim/bundle` 即可。然后按照官方的教程
配置一些参数。可是最后好像不生效。Google 了半天，发现有同样情况的人，应该是依赖了 `conceal` 这个
特性。有两个方式可以查看使用的 Vim 是否支持：

在命令行：

```bash
vim --version
```

会发现 conceal 前面是一个减号(-)，表示不支持

在 Vim 中：

```bash
echo has('conceal')
```

会发现输出 0，表示不支持

### 解决方法

#### 从源码编译，使得支持

#### 直接使用 brew 安装的 vim 也可以 work

```bash
brew install vim
```

安装后将 vim 重定向到自己安装的 vim 就行。我是自己做了一个 alias。

![效果](/images/tools/vim/indent-line-effect.png)

<a id="bp-not-working"></a>

### backspace 失效

使用从 `brew` 安装的代码后，好像回退键(backspace) 失效了。解决方法

```vim
set backspace=indent,eol,start
```

本文完
