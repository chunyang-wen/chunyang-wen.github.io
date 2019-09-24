---
layout: post
title: git basics
categories: [blog, tools]
tags: [tools]
---


Git最初的作者是Linux内核的开发者Linus。之前linux内核维护是使用bitkeeper，但是他们发现有人在反编译bitkeeper，收回了对开源的特权。所以开源社区需要开发一个属于自己的版本控制工具，然后Git就诞生了。

### Git 初探 ###

Git与传统的中心控制的版本控制工具不同点是，它是分布式的。每个人都有完整的库，如果某个仓库崩溃了，可以使用仍和一个库来恢复。Git的工作原理可以分为三个阶段：


+ working directory
   即我们的工作目录，这里面有各种文件，包括被版本控制系统tracking的和没有被tracking的。

```shell
git checkout branch_name/clone repository_url
```

+ staging area
   文件的增删或者修改通过下面命令等命令

```shell
git add file_name/directory
```

+ git directory
   将所做的修改提交到git的仓库

```shell
git commit -m msg
```

上面的三个过程其实就已经表明git的一些基本操作，如果需要了解更详细的内容可以参考文末提供的参考链接。


### 使用github ###

现在比较受欢迎的开源代码寄存网站Github，它使用的就是git的版本控制。当我们在github上发现一个我们喜欢的库时，我们可以将其克隆到本地，使用source insight等工具查看源码。当然也可以针对自己创建的代码库，进行修改。

#### 拷贝代码到本地 ####

```shell
git clone repository_url
```

#### 将修改加入staging area ####

```shell
git status
git add file_name/.
```

使用git add命令就可以将我们做的修改加入staging area，也可以增加新的文件。`git status`是查看目前的状态


#### 提交修改 ####

```shell
git commit -m msg
```

后面的-m表示本次提交的信息。如果不加-m，则会打开默认编辑器，让你编辑提交信息


#### 修改提交到远端 ####

```shell
git push
```

这个时候可能会让你输入用户名和密码。可以通过配置一下，让git记住用户名和密码，以后就不用输入了。

```shell
git config --global credential.helper store
```

至此，我们已经完成一个简单的循环了，从克隆代码，修改，提交，提交到远端。在学会上面基本命令后，我们还要学习如何恢复修改，回滚版本库，merge，diff等使用。

### 在Github上建立个人主页 ###

现在博客可能已经不像以前那样受欢迎，但是搭建一个属于自己的博客，学会使用markdown语法还是一件让人觉得有收获的事情。我之前的博客也是clone的别人。大家首先可以将我的博客进行clone，然后提交到自己的仓库。具体教程可以见文末提供的链接。

在这里我指出一些修改要注意的地方：
+ 博客位置
   看一下_posts文件夹里面的格式就好
+ 增加配图
   在assets/image中添加图片，然后使用markdown语法，图片路径是/assets/image/xx.jpng
+ 克隆博客，修改相关页面
   about/index.md

当然，我只是毛遂自荐，你也可以clone其它人的博客，欢迎交流好用的模板。


### 参考链接

+ [Git思想和基本工作原理](http://www.nowamagic.net/academy/detail/48160210 "nowmagic" )
+ [Git clone命令](http://blog.csdn.net/techbirds_bao/article/details/9179853 'csdn' )
+ [Github pages](https://pages.github.com/ 'github' )



