---
layout: post
title: Add custom domain for github pages
categories: [blog, git]
tags: [reading]
redirect_from:
 - /gh-pages/domain-for-gh-pages
---

由于特殊原因，导致自己的 VPS 无法访问。

[检测网址](http://port.ping.pe/)

这个网站会从各个地方来探测你的机器某个端口的可连接性。我基本上从中国发出的连接都失败了。
咨询了客服，客服说由于 IP 被封，停止相关的服务后，在几天或者几周后，IP 可能会被解封。

上述失败引发我的思考。这个 VPS 其实发挥了两个作用：

+ 个人博客
+ 特殊用途

Linux 的设计原则是单一职能原则，这里我本不该将这两个东西放在一起。因为特殊用途是有点风险的，可能
会影响正常的博客被阅读，而且由于 IP 时常存在被封的风险，网站的可用性会降低很多。花时间研究了下
`Github pages` 的 CNAME 配置。说句实话，文档太过详实，不知道该从哪入手。

最有用的 [Trouble shooting 页面](https://help.github.com/en/articles/troubleshooting-custom-domains)

### 第一步

在对应 `Github pages` 上有个 `settings` 按钮，点击后往下拉，会让你设置 Github Pages。默认的发布域名
是： `[your-user-name].github.io`。可以自定义域名，输入自定义的域名后，会自动往 repo 的根目录放置
一个文件，`CNAME`，全大写。里面的内容是你指定的域名。

### 第二步

配置结束后，其实仍然没法使用自定义的域名来访问。需要去 DNS 服务商（购买域名的地方）增加一些记录，
这里增加的记录分为两类：

+ A 记录：域名到 ip 的映射
+ CNAME： 域名到域名的映射

一般可能我们增加一个 CNAME 映射应该就可以了：

> CNAME: your-custom-domain->[your-user-name].github.io

当 CNAME 生效时，会自动展现你的 Github pages。**新增记录实时生效（取决你的域名服务商的发布频率），
改记录要看情况，一般过了 TTL 后可能会生效**

### 第三步

打开你的域名 https (Enforce HTTPS). 此时你应该使用如下 ip 记录：(A 记录)

> 185.199.108.153
>
> 185.199.109.153
>
> 185.199.110.153
>
> 185.199.111.153

如果使用的是旧的 `192.30.252.153` 或者 `192.30.252.154` 需要用上面新的地址

如果使用的是 CNAME，应该不用配置这个 A 记录

### 总结

至此，个人博客是恢复了。而且依赖于 Github 的强大功能，可用性会得到很大提高，而且还有 CDN 的加速，
强制 HTTPS（之前自己使用 nginx，使用的是 [`ertboot`](https://certbot.eff.org/) 来管理）。

本文完
