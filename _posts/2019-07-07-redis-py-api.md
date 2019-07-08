---
layout: post
title: Reids python API cheatsheet
categories: [python]
tags: [redis]
---

+ [Introduction](#intro)
+ 主要的类和函数
  + [Redis, StrictRedis](#a)
  + [Monitor](#b)
  + [Pubsub, PubSubWorkerThread](#c)
  + [Pipeline](#d)
  + [Script](#e)
  + [BitFieldOperation](#f)


<a id="intro"></a>

### Introduction

本文主要介绍 `Redis` 的 Python API 的常见使用方法。Python API 也是具体 Redis 命令的包装。
只不过是实现了支持 Redis 协议的功能。

### 主要的类和函数

<a id="a"></a>

#### Redis, StrictRedis

要连接上 Redis 服务器，需要知道三个元素：
+ host
+ port
+ password: 如果服务端设置了密码

主要接口如下：

##### 构造对象

+ `pipline(self, transaction=True, shard_hint=None)`
+ `lock(self, name, timeout=None, sleep=0.1, blocking_timeout=None, lock_class=None, thread_local=True)`
+ `pubsub(self, **kwargs)`
+ `monitor(self)`

下述的调用都是 `execute_command(self, *args, **options)` 来完成。

#### 保存

+ `bgrewriteaof(self)`
+ `bgsave(self)`

#### Client 相关操作

+ `client_kill(self, address)`
+ `client_kill_filter(self, _id=None, _type=None, addr=None, skipme=None)`
+ `client_list(self, _type=None)`: 类型可以是： normal，master，replica，pubsub
+ `client_getname(self)`
+ `client_id(self)`
+ `client_setname(self, name)`
+ `client_unblock(self, client_id, error=False)`
+ `client_pause(self, timeout)`

#### 基础命令

+ `append(self, key, value)`
+ `get(self, name)`
+ `getrange(self, key, start, end)`
+ `getset(self, name, value)`
+ `set(self, name, value, ex=None, px=None, nx=False, xx=False)`
+ `setex(self, name, time ,value)`
+ `setnx(self, name ,value)`
+ `setrange(self, name, offset, value)`: 覆盖从 `offset` 开始的内容
+ `decr(self, key, amount=1)`
+ `decrby(self, name, amount=1)`
+ `incr(self, name, amount=1)`
+ `incrby(self, name, amount=1)`
+ `incrbyfloat(self, name, amount=1.0)`

+ `psetex(self, name, time_ms, value)`
+ `pttl(self, name)`
+ `ttl(self, name)`
+ `type(self, name)`
+ `strlen(self, name)`
+ `substr(self, name, start, end=-1)`
+ `touch(self, *args)`: 更新最近的访问时间，不存在的 key 会被忽略
+ `randomkey(self)`
+ `rename(self, src, dst)`
+ `renamenx(self, src, dst)`
+ `restore(self, name, ttl, value, replace=False)`
+ `unlink(self, *names)`

+ `watch(self, *names)`: **Deprecated**，使用 `Pipeline`
+ `unwatch(self)`: **Deprecated**，使用 `Pipeline`

+ `bitcount(self, key, start=None, end=None)`
+ `getbit(self, name, offset)`
+ `setbit(self, name, offset, value)`
+ `bitfield(self, key, default_overflow=None)`
+ `bitop(self, operation, dest, *keys)`
+ `bitpos(self, key, bit, start=None, end=None)`

+ `mget(self, keys, *args)`
+ `mset(self, mapping)`: mapping 是 `dict`
+ `msetnx(self, mapping)`

+ `blpop(self, name, timeout=0)`
+ `brpop(self, name, timeout=0)`
+ `brpoplpush(self, src, dst, timeout=0)`
+ `lindex(self, name, index)`
+ `linsert(self, name, where, refvalue, value)`
+ `llen(self, name)`
+ `[l/r]pop(self, name)`
+ `[l/r]pushx(self, name, *values)`
+ `[l/r]range(self, name, start, end)`
+ `lrem(self, name, count, value)`
+ `lset(self, name, index, value)`
+ `ltrim(self, name, start, end)`: 删除 start 和 end 之间的内容
+ `rpoplpush(self, src, dst)`
+ `sort(self, name, start=None, num=None, by=None, get=None, desc=False, alpha=False, store=None, groups=False)`

+ `sadd(self, name, *values)`
+ `scard(self, name)`
+ `sdiff(self, keys, *args)`
+ `sdiffstore(self, dest, keys, *args)`
+ `sinter(self, keys, *args)`
+ `sinterstore(self, dest, keys, *args)`
+ `sismember(self, name, value)`
+ `smembers(self, name)`
+ `smove(self, src, dst, value)`
+ `spop(self, name, count=None)`
+ `srandmember(self, name, number=None)`
+ `srem(self, name, *values)`
+ `sunion(self, keys, *args)`
+ `sunionstore(self, dest, keys, *args)`

+ `hdel(self, name, *keys)`
+ `hexists(self, name, key)`
+ `hget(self, name, key)`
+ `hgetall(self, name)`
+ `hincrby(self, name, key, amount=1)`
+ `hincrbyfloat(self, name, key, amount=1.0)`
+ `hkeys(self, name)`
+ `hvals(self, name)`
+ `hlen(self, name)`
+ `hset[nx](self, name, key, value)`
+ `hmset(self, name, mapping)`
+ `hmget(self, name, keys, *args)`
+ `hstrlen(self, name, key)`

**Need to understand what zset means**

+ `zadd(self, name, mapping, nx=False, xx=False, ch=False, incr=False)`
+ `zcard(self, name)`
+ `zcount(self, name, min, max)`
+ `zincrby(self, name, amount, value)`

+ `scan(self, cursor=0, match=None, count=None)`: scan list
+ `scan_iter(self, match=None, count=None)`: scan list
+ `sscan(self, name, cursor=0, match=None, count=None)`: scan set
+ `sscan_iter(self, name, match=None, count=None)`
+ `hscan(self, name, cursor=0, match=None, count=None)`: scan dict
+ `hscan_iter(self, name, match=None, count=None)`
+ `zscan(self, name, cursor=0, match=None, count=None, score_cast_func=float)`
+ `zscan_iter(self, name, match=None, count=None, score_cast_func=float)`

+ `delete(self, key)`
+ `dump(self, name)`
+ `move(self, name, db)`
+ `persist(self, name)`
+ `exists(self, *names)`
+ `expire(self, name, time)`
+ `expireat(self, name, when)`
+ `pexpire(self, name, time)`
+ `pexpireat(self, name, when)`
+ `keys(self, pattern='*')`

#### Sentinel 相关

+ `sentinel_get_master_addr_by_name(self, service_name)`
+ `sentinel_master(self, master)`
+ `sentinel_masters(self)`
+ `sentinel_monitor(self, name, ip, port, quorum)`: add a new node to be monitored
+ `sentinel_sentinels(self, service_name)`
+ `sentinel_set(self, name, option, value)`
+ `sentinel_slaves(self, service_name)`

#### 其它

+ `echo(self, value)`
+ `dbsize(self)`
+ `flushall(self, asynchronous=False)`: 删除 Host 上所有键
+ `flushdb(self, asynchronous=False)`: 删除指定 database 上所有键
+ `swapdb(self, first, second)`
+ `info(self, section=None)`
+ `ping(self)`
+ `save(self)`
+ `shutdown(self)`
