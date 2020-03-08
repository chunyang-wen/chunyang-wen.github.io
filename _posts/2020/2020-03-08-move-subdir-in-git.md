---
layout: post
title: Move subdirectory of a git repository and keep commit message
categories: [blog, tools]
tags: [git]
---

How to extract a subdirectory of a git repository and keep its commit message? If we directly
`move` everything and `add` them again, we will lose all the history we had.

+ TOC
{:toc}

### Introduction

Recently in my project, I have to (or plan to) move a subdirectory out of a large git repository.
But I want to keep the history. Also I will change the module name. By the way, it is a python
module and I am refactoring work.

### Generate the history as a patch and apply the patch

[Reference](https://stackoverflow.com/questions/1365541/how-to-move-files-from-one-git-repo-to-another-not-a-clone-preserving-history)

```shell
cd path/to/repository
git log --pretty=email --patch-with-stat --reverse --full-index --binary -- path/to/file_or_folder > /path/to/patch

cd path/to/another_repository
git am --committer-date-is-author-date < /path/to/patch
```

#### Handling merge commit

Add `-m --first-parent` when generating the history.

#### Change module name

Actually it is simple. Just find the pattern and replace it.

```shell
sed -i "s/src/replace/g" `grep "src" -rl /path/to/dir`
```

Have fun!
