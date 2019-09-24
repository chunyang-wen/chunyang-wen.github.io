---
layout: post
title: Nginx server and location selection
categories: [blog, nginx]
tags: [reading]
---

+ [Introduction](#i)
+ [Server](#s)
  + [Listen 匹配](#li-m)
  + [Server 匹配](#se-m)
+ [Location](#l-m-r)
  + [修饰符](#l-m)
  + [匹配规则](#m-r)
  + [Location 之间跳转](#redirect)

<a id="i"></a>

### Introduction

一个 `server` 块表示如何处理指定类型的请求，根据如下信息：

+ ip: 默认 `0.0.0.0`
+ port: 默认 `80`
+ server\_name: 会和请求中的相比较

一个 `location` 块是位于具体的 `server` 内部，告诉 Nginx 如何处理不同的资源和 URI。URI 可以根据需求
任意的切分。

<a id="s"></a>

### Server

配置中可以同时存在多个 `server` 配置块，Nginx 有一套规则来选择最佳的匹配，主要依赖：

+ `listen`
+ `server_name`

`listen` 可以设置如下的值：

+ `ip+port`: `listen 190.22.22.11:8080`
+ `ip`: 端口默认 80
+ `port`: ip 默认是 `0.0.0.0`
+ path/to/a/Unix/socket: 多个 server 之间传递请求

<a id="li-m"></a>

#### Listen 匹配
当确定 `server` 块时，Nginx 首先依赖 `listen` 中的配置，基于如下规则：

+ 给不完整的 `listen` 描述不全
+ 基于请求中的 ip 和 port 来匹配最具体(most specially)的 `server` 块。
+ 如果只有一个匹配，会直接使用。如果存在多个，则会使用 `server_name` 来决定

<a id="se-m"></a>

#### Server 匹配

请求的 `Host` 头部会有请求的域名或者 ip 地址，匹配规则如下

+ 精确匹配
+ 在前面增加\*，继续匹配
+ 在后面增加\*，继续匹配
+ 匹配正则的 `server_name`，使用 `~` 来表示
+ 使用 `default_server`

<a id="l-m-r"></a>

### Location

```bash
location optional_modifier location_match {

}
```

<a id="l-m"></a>

#### 修饰符

上述是 `location` 块的基本配置格式。常见的 `optional_modifier` 如下：

+ (none): 空，`location_match` 会被识别成前缀，即匹配这些字符串在 URI 的开头部分。
+ "=": 精确匹配，当精确匹配匹配成功后会立即停止搜索
+ "~": 大小写敏感的正则匹配
+ "~\*": 大小写不敏感的正则匹配
+ "^~": 如果是最优的非正则配，则不会触发正则匹配

<a id="m-r"></a>

#### 匹配规则

部分匹配发生后会立即停止匹配，有些会继续搜索。具体顺序如下：

1. 前缀匹配，每个 `location` 都会和 URI 比较
2. 精确匹配(=)，如果精确匹配成功，直接停止匹配
3. 如果没有精确匹配发生，从最长的匹配前缀位置开始
  + 如果最长匹配使用了 `^~` 最为修饰，会立即停止匹配
  + 存储当前匹配，继续搜索
4. 一旦选择和存储了最长前缀匹配，nginx 会继续评估大小写敏感和大小写不敏感的正则位置。选择第一个匹配
的位置
5. 如果没有匹配恒泽，之前存储的前缀匹配会起作用

<a id="redirect"></a>

#### Location 之间跳转

如下四个配置描述可能会触发在 Location 之间的跳转：

+ index: `index index.html`
+ try\_files: `try_files $uri $uri.html $uri/ /fallback/index.html;`
+ rewrite: `rewrite ^/rewriteme/(.*)$ /$1 last;`
  + rewrite 后面参数可配：`last`, `break`, `permanent`
+ error\_page: `error_page 404 /another/whoops.html;`

本文主要参考资料如下，主要是翻译前两篇文章

+ [Nginx Location Directive Explained](https://www.keycdn.com/support/nginx-location-directive)
+ [Understanding Nginx Server and Location Block Selection Algorithms](https://www.digitalocean.com/community/tutorials/understanding-nginx-server-and-location-block-selection-algorithms)
+ [Nginx Beginner's Guide](http://nginx.org/en/docs/beginners_guide.html)
+ [Nginx core module location](http://nginx.org/en/docs/http/ngx_http_core_module.html#location)

