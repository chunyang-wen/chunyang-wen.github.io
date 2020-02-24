---
layout: post
title: Code Rush观后感
categories: [blog, movies]
tags: [reading]
redirect_from:
 - /movies/thoughts-of-code-rush
---


在等待吃饭的间隙把电影《Code Rush》看了一下，这个电影也是Jeff Atwood和阮一峰推荐的。故事的主要内容时Netscape将浏览器代码开源为Mozilla的过程。

网景公司制造了互联网公司的神话，在IPO的时候股价从20$一下子飙升至170多$。一下子让很多人成了富翁，也许这也是很多人愿意加入初创公司的原因，也为有一夜暴富的可能性。但是不知道是不是微软公司是故意的还是像Bill Gates所说的，他们不想阻止人们自由使用软件的权利。不管怎么说，微软还是利用自己在操作系统上的帝国地位完成了对网景公司的逆袭。虽然后来微软在预装软件上对浏览器采用投票的方式决定，但是可能大势已去。

网景公司知道自己在浏览器市场已经无法和微软帝国抗衡，CEO选择了将浏览器代码开源，同时支持三个平台，对于这个计划的日期定在3月31日早上10点，开放对用户的下载。在这个时间确定了以后，其实开源的代码还有很多工作需要完成，消除BUG，完成对各种平台的支持，而且要保证软件可以正常运行。

在项目截止日期还有一个月的时候，他们每个人负责自己的工作，虽然他们的工作可能不同，但是他们的在那个时候的结论是一致的，“There are doomed!”，他们死定了，因为按时发布软件似乎就是一个不可能的过程，无数的BUG，而且BUG在持续增加。有些人白天上班，有些人是夜猫子。大家都是筋疲力尽。

在这个关键时刻，还有一个程序员处于missing的状态，让大家更为着急。等到他回来的时候，项目领导者下了最后命令，必须完成，它是优秀的人，果然在一夜之间就解决了他自己的BUG。距离发布的前一天，整个团队终于将这个不可能完成的任务完成了，开始第一次在普通机器上的调试。

结果让人欢心鼓舞。但是瞬间crash了。没事，至少代码是可以运行的。

好事总是多磨，在发布的前一天，发现有一段代码时Apple，必须得到Apple的授权。他们致电给Jobs，但是好像电话没有通。最后又是那个消失的程序员完成了代码的重写。

他们觉得网景公司将浏览器代码开源是一件非常重大的事情，但是当他们联系媒体的时候，似乎不怎么受待见。媒体都认为网景已经不是以前的网景了。

在发布前1分钟，突然连不上ftp服务器，无法将代码送至指定服务器供用户下载。但是好在是虚惊一场。最后还是成功的发布了。

网景公司的开源助长了开源力量。而且也使得微软的敌人从网景公司变成了开源的群体。这是一个互联网历史上需要铭记的事件与时刻。

那些年，网景公司V5的程序员；那些年网景公司开明的决定，将浏览器源代码开源，并且成立了日后不断壮大的Mozilla基金会。

本文完