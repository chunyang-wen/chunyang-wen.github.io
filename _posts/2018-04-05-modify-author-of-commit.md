---
title: 改变之前 commit 的信息
layout: post
categories: [blog, git]
tags: [git]
---

+ [综述](#intro)
+ [简单暴力的方法](#simple-force)
+ [优雅的方法](#gentle-way)
+ [rebase 功能](#rebase-func)

<a name="intro"></a>

### 综述

今天同事遇到一个问题：仓库中限制在提交时必须使用公司内部的邮箱。但是由于之前没有配置：

+ git config --global user.name
+ git config --global user.email

导致之前的信息有误。其分支图如下：

```bash
A->B-C->HEAD
```

其中 B 和 C 两次 commit 的作业是有问题的。所以需要修改。

<a name="simple-force"></a>

### 简单暴力的方法

最直观的解决方法是：`git reset A`，然后重新 add 更改的文件，重新做一次新的 commit。这样做法的优点
是十分简单，重来一次；缺点是会丢掉两次 commit 的具体信息。

#### 流程

```shell
git reset A # DO NOT add --hard, on your own risk if you do
git add any-new-file
git add -u . # changed file
git commit -m 'your commit message'
```

当然你也可以重做两次，这样所有东西都会重新回来。

<a name="gentle-way"></a>

### 优雅的方法

[参考链接](https://stackoverflow.com/questions/3042437/change-commit-author-at-one-specific-commit)

其主要是使用 `rebase` 的命令。`rebase` 命令会重放 rebase commit 之后的所有 commit。这样在重放的时候
我们就有机会去改变对应的信息。

```bash
git rebase -i A
```

这个时候会跳出来一个编辑框：pick/squash/edit/drop/exec(自己增加执行的命令)

+ p, pick = use commit
+ r, reword = use commit, but edit the commit message
+ e, edit = use commit, but stop for amending
+ s, squash = use commit, but meld into previous commit
+ f, fixup = like "squash", but discard this commit's log message
+ x, exec = run command (the rest of the line) using shell
+ d, drop = remove commit

我们选择 edit，这样在每次重放 commit 时，会允许我们去编辑相应的信息。

```bash
git commit --amend --author="Author Name <email@address.com>"
git rebase --continue
```

其中 `--author` 的格式必须按照那个上述命令中的样式，否则会校验错误。

会在 B 和 C 处都停留。所以编辑两次就好了。Bingo！

<a name="rebase-func"></a>

### rebase 功能

`rebase` 是 git 里面一个比较神奇的功能。一般使用户多个分支开发的时候，想重新改变自己的分支起点。

```bash
A--->B--->C--->D
     |--->E--->F
```

上图中，上面是 master 分支。我们从 master 上的 B 分支出来，往前开发到 F。但是 master 分支也在往
前走。如果这个时候想应用 master 分支的更新，从 D 开始我们的开发。则我们需要在我们的分支上 `rebase`
master 分支。

```bash
A--->B--->C--->D-->
               |--->E--->F
```

更加详细的描述： `git help rebase`

### 常用的功能

+ git rebase another-branch
+ git rebase --continue
+ git rebase --skip
+ git rebase --abort

本文完。Enjoy it.

