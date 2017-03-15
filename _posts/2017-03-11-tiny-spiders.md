---
layout: default
title: awk + wget 实现的简单爬虫
categories:
- tools
tags:
- linux
- shell
---

在很多人眼中，**爬虫**可能是一个非常厉害的东西，它的编写肯定会非常的复杂。当然 Google 和 Baidu 的爬虫
历经那么多次迭代，其系统整个流程肯定会非常的完善和复杂。万里之行，始于足下。

之前花了点时间制作了一个简单的小爬虫，它的功能：

+ 第一次全量地从某个网站下载全部的 PDF 文件 （关于去水印
见另外一篇文章）
+ 每天例行更新 PDF 文件
+ 例行更新 PDF 文件后自动上传至百度网盘（[bypy](https://github.com/houtianze/bypy)）
+ 发送更新的文件列表至邮箱

这个项目的页面在 [TOY-Spiders](https://github.com/chunyang-wen/toy-spiders/tree/master/AllItEbooksInfo)

抓取的网址是 **[www.allitebooks.com](http://www.allitebooks.com)**。首先感谢这个网站提供这么一个免费的 PDF
分享平台，十分怀念之前的**皮皮书屋**。

这个网站可以检索你感兴趣的电子书，如果找到合适的可以点击下载或者在线阅读。
由于它的检索功能不是很强大，所以想把它所有数据都下载下来，一方面方便阅读，另外一个方面自己可以建立其它的索引来
查找文件（*Everything*，强烈案例）。

使用 *Chrome* 来分析[下载的页面](http://www.allitebooks.com/beginning-python-3rd-edition/)，
发现其提供的是一个完整的 [URL](http://file.allitebooks.com/20170307/Beginning%20Python,%203rd%20Edition.pdf) 链接。于是尝试 wget 尝试下；

```shell
wget URL -o hah.pdf
```

发现可以正常下载。如果能够获取全站的所有 PDF 的下载链接即可将全站的 PDF 文件下载。简单分析这个网站有两种组织
PDF的方式：

+ 分类后分页浏览
+ 首页分页浏览

通过分析几个分类分页的浏览网址，发现最终 PDF 页面的链接和分类没有关系；首页的分页浏览包括了所有的 PDF。通过
*Chrome*的工具（查看元素/Inspect element）发现展示页面链接的 Tag = 'entry-title'，即使用正则找到这一行，
然后这一行中有超链接就是文档的展示链接。点开文档的展示链接，查看源码发现：真正的下载链接是后缀有 *.pdf*的字样。

到此为止所有分析就结束了，从首页分页浏览开始

+ 每一页找到所有的展示链接
+ 进入每个展示链接，找到 *.pdf* 为后缀的下载链接下载即可

通过分析就是两句 *awk* 命令：

```shell
# 提取分页浏览中每页中包含entry-title的展示页面
awk '$0~/entry-title/ && $0!~/--/' ${PagesView} | awk -vFS='"' '{print $4}' > ${DisplayURLEachPage}
# 从每个展示页面中提取下载的链接
awk -vFS='"' '$0~/\.pdf/{print $2}' ${DisplayURLEachPage}
```

至此下载链接已经分析出来，接下来就是 codingnow 时间。整个过程需要注意的是保证出错后程序可以继续执行，错误类型：

+ 下载失败
+ 提取某些下载链接错误
+ 下载的间隔不要太频繁，防止被封杀

具体代码大家可以去看看这个 [repo](https://github.com/chunyang-wen/toy-spiders)

完整下载工作后，将数据备份至百度网盘，这个过程还是挺费事的。

+ 网盘非会员一次只能上传 500 个文件 （哎），写了个split.sh脚本把文件切分下，然后挨个文件夹往上拖。
+ 所有的网络都是走 VPN（本次任务不需要走 VPN），所以速度受限（幸亏没人查水表。）

后续改进的地方：

+ 第一次全量抓取后就考虑后续的增量更新。该网站每次都将最新的数据放到首页分页浏览的前面，这样就过分析出要下载的
数据是否已经下载过（`grep file filecollection`）就可以了。
+ 上传至到百度网盘的过程希望自动化，[bypy](https://github.com/houtianze/bypy)这个项目完美地解决了我的问题。本来
打算自己申请个开发者权限，然后利用 API 去上传文件，但是百度的开发者网站实在是不太友好，而且接口申请也一直在
pending状态。bypy已经够用。
+ 自动更新结束后希望有邮件通知我更新了哪些书籍，如果更新的书籍中有自己喜欢的，就可以及时去看了。所用的操作系统是
Ubuntu，安装 msmtp和mutt后就可以发送简单的文本邮件了。


```shell
cat Msg | mutt -s 'updated books' your@email
```

关于这些配置放在[mail-config](https://github.com/chunyang-wen/config-collections/tree/master/mail)，
感兴趣的自取。

最后一步就大功告成，没错，`crontab`

```shell
00 11 * * * cd downloaddir;nohup sh download.sh &> update.log &
```

每天11点例行更新，更新完就收到邮件更新通知。

回过头来思考整个过程，其实对于这些不是一开始就所有东西都设计好的。每完成一步工作就会有新的想法来完善。后面准备系统得学习一个 `Python` 的爬虫工具 `scrapy`。因为这次的代码有很多硬编码，扩展性不是很强。

> 没有最好的工具，满足需求就是好的。

预告一下：后面会写大概4个主题，顺序不固定，

+ awk & sed：把编写的一些工具以及笔记整理下，sed好像很少，因为正则总是记不住。
+ Python: 经典的库的使用，做了很多笔记。在整理的过程中和大家一起学习。
+ Memcached / Redis：读了代码，分别写一下自己的理解。Redis有黄章的书，买了还没读。

争取每周可以更新两篇。

本文完
