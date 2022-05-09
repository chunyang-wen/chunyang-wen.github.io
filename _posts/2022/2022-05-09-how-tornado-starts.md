---
layout: post
title: How tornado starts?
categories: [blog, python]
tags: [blog, python]
---

项目中的服务使用 `tornado` 来搭建，但是对于 `tornado` 如何启动还没有仔细研究过。
在某次问题排查时，仔细研究了 `tornado` 是如何启动的。

+ toc
{:toc}


在 tornado 的大部分文档是建议使用

```python
from tornado.ioloop import IOLoop

IOLoop.current().start()
```

上述程序会启动后端的 `HTTPServer`。`HTTPServer` 派生自 `TCPServer`。如果需要依赖这个功能来调用
`start()`，那么在 `TCPServer`的实现中，`start()`一定会被调用。为了看清楚这个调用关系，
在 `start` 函数入口加一句抛异常。但是奇怪的是：服务启动后，异常并没有抛出，tornado 服务运行正常。

![image.png](/images/python/head.png)

## 测试

为了验证 tornado 到底是怎么启动服务的，写了简单的服务，代码如下，保存为 app.py.

```bash
python app.py  # 启动 8000 端口的服务
```

```python
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop


class Handler(RequestHandler):

    def get(self):
        print("Handle request")
        self.write("Bingo!")


url_specs = [
    ("/", Handler),
    ("/a", Handler),
]

app = Application(url_specs)


port = 8000
app.listen(port)
print(f"Listen on port {port}")

IOLoop.current().start()

```

### 刨根问底

其实 `app.listen()`的实现就是创建 `HTTPServer`，然后调用 `TCPServer`的
`listen` 接口。这里的 `listen` 实现：

```python
def listen(self, port: int, address: str = "") -> None:
    """Starts accepting connections on the given port.

        This method may be called more than once to listen
        on multiple ports.
        `listen` takes effect immediately; it is not necessary to call
        `TCPServer.start` afterwards.  It is, however, necessary to start
        the `.IOLoop`.
        """
    print(f"Listen for tcp server")
    sockets = bind_sockets(port, address=address)
    self.add_sockets(sockets)

```

这里其实开始绑定端口。这里的 `add_sockets`函数比较关键，因为是它开始把
socket 上事件挂载到 `IOLoop.current()` 上。

```python
def add_sockets(self, sockets: Iterable[socket.socket]) -> None:
    """Makes this server start accepting connections on
        the given sockets.

        The ``sockets`` parameter is a list of socket objects such as
        those returned by `~tornado.netutil.bind_sockets`.
        `add_sockets` is typically used in combination with that
        method and `tornado.process.fork_processes` to provide greater
        control over the initialization of a multi-process server.
        """
    for sock in sockets:
        self._sockets[sock.fileno()] = sock
        self._handlers[sock.fileno()] = add_accept_handler(
            sock, self._handle_connection
        )

```

`add_accept_handler`是开始挂载事件：

```python
def add_accept_handler(
    sock: socket.socket, callback: Callable[[socket.socket, Any], None]
) -> Callable[[], None]:
    """Adds an `.IOLoop` event handler to accept new connections
    on ``sock``.

    When a connection is accepted, ``callback(connection, address)``
    will
    be run (``connection`` is a socket object, and ``address`` is the
    address of the other end of the connection).  Note that this
    signature
    is different from the ``callback(fd, events)`` signature used for
    `.IOLoop` handlers.

    A callable is returned which, when called, will remove the `.IOLoop`
    event handler and stop processing further incoming connections.

    .. versionchanged:: 5.0
       The ``io_loop`` argument (deprecated since version 4.1)
       has been removed.

    .. versionchanged:: 5.0
       A callable is returned (``None`` was returned before).
    """
    io_loop = IOLoop.current()
    removed = [False]

    def accept_handler(fd: socket.socket, events: int) -> None:
        # More connections may come in while we're handling callbacks;
        # to prevent starvation of other tasks we must limit the number
        # of connections we accept at a time.  Ideally we would accept
        # up to the number of connections that were waiting when we
        # entered this method, but this information is not available
        # (and rearranging this method to call accept() as many times
        # as possible before running any callbacks would have adverse
        # effects on load balancing in multiprocess configurations).
        # Instead, we use the (default) listen backlog as a rough
        # heuristic for the number of connections we can reasonably
        # accept at once.
        for i in range(_DEFAULT_BACKLOG):
            if removed[0]:
                # The socket was probably closed
                return
            try:
                connection, address = sock.accept()
            except BlockingIOError:
                # EWOULDBLOCK indicates we have accepted every
                # connection that is available.
                return
            except ConnectionAbortedError:
                # ECONNABORTED indicates that there was a connection
                # but it was closed while still in the accept queue.
                # (observed on FreeBSD).
                continue
            callback(connection, address)

    def remove_handler() -> None:
        io_loop.remove_handler(sock)
        removed[0] = True

    io_loop.add_handler(sock, accept_handler, IOLoop.READ)
    return remove_handler

```

回过头，我们再来看 `IOLoop.current().start()`做的事情：

```python
@staticmethod
def current(instance: bool = True) -> Optional["IOLoop"]:
    """Returns the current thread's `IOLoop`.

        If an `IOLoop` is currently running or has been marked as
        current by `make_current`, returns that instance.  If there is
        no current `IOLoop` and ``instance`` is true, creates one.

        .. versionchanged:: 4.1
           Added ``instance`` argument to control the fallback to
           `IOLoop.instance()`.
        .. versionchanged:: 5.0
           On Python 3, control of the current `IOLoop` is delegated
           to `asyncio`, with this and other methods as pass-through
           accessors.
           The ``instance`` argument now controls whether an `IOLoop`
           is created automatically when there is none, instead of
           whether we fall back to `IOLoop.instance()` (which is now
           an alias for this method). ``instance=False`` is deprecated,
           since even if we do not create an `IOLoop`, this method
           may initialize the asyncio loop.
    """
    try:
        loop = asyncio.get_event_loop()
    except (RuntimeError, AssertionError):
        if not instance:
            return None
        raise
    try:
        return IOLoop._ioloop_for_asyncio[loop]
    except KeyError:
        if instance:
            from tornado.platform.asyncio import AsyncIOMainLoop

            current = AsyncIOMainLoop(make_current=True)
            # type: Optional[IOLoop]
        else:
            current = None
    return current


def start(self) -> None:
    """Starts the timer."""
    # Looking up the IOLoop here allows to first instantiate the
    # PeriodicCallback in another thread, then start it using
    # IOLoop.add_callback().
    self.io_loop = IOLoop.current()
    self._running = True
    self._next_timeout = self.io_loop.time()
    self._schedule_next()
```

本质上做的事就是将 `asyncio.get_event_loop()`包装到 `AsyncIOMainLoop`。
这个 `AsyncIOMainLoop`的 `start`函数是调用 `event_loop` 的 `run_forever`。
通过以上分析后，其实我们并不需要调用 `IOLoop.current().start()`，我们可以直接利用
`asyncio`的接口来启动即可。本质是 tornado 把 tcp 的事件绑定到 event loop 上。

### 最终代码

```python
import asyncio
from tornado.web import Application, RequestHandler


class Handler(RequestHandler):

    def get(self):
        print("Handle request")
        self.write("Bingo!")


url_specs = [
    ("/", Handler),
    ("/a", Handler),
]

app = Application(url_specs)


port = 8000
app.listen(port)
print(f"Listen on port {port}")

asyncio.get_event_loop().run_forever()

```

## get_event_loop

`get_event_loop` 又在做什么事呢？
如下两个文件：`asyncio/events.py` 和 `asyncio/unix_events.py` 中描述怎么拿到对应的 `event_loop`

`base_events.py`: `run_forever`, `run_until_complete`

## stop

```python
IOLoop.current().stop()
```

实际上是 Mark 标记，然后由具体的 eventloop 来关闭

```python
def run_forever(self):
    """Run until stop() is called."""
    self._check_closed()
    self._check_runnung()
    self._set_coroutine_origin_tracking(self._debug)
    self._thread_id = threading.get_ident()

    old_agen_hooks = sys.get_asyncgen_hooks()
    sys.set_asyncgen_hooks(firstiter=self._asyncgen_firstiter_hook,
                           finalizer=self._asyncgen_finalizer_hook)
    try:
        events._set_running_loop(self)
        while True:
            self._run_once()
            if self._stopping:
                break
    finally:
        self._stopping = False
        self._thread_id = None
        events._set_running_loop(None)
        self._set_coroutine_origin_tracking(False)
        sys.set_asyncgen_hooks(*old_agen_hooks)
```

## 总结

+ 启动实际上
  + `listen`: 把时间挂载到 `event_loop` 中
  + `start` 调度下一个 event
+ 结束
  + 标记，依赖底层的 event loop 去执行。按照这个逻辑，岂不是只要事件不退出，这个 stop
  就结束不了？
