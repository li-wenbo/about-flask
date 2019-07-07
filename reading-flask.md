# A web site using Flask Framework
![a web site](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/a-web-site.png)
====
 * Flask for service logic
 * Gunicorn hosts the flask app
 * Finally nginx esponsible for：
   * buffer slow clients on the Internet
   * load balance for many gunicorn processes
   * WAF and so on 

# How it works

* pep333
  
# pep333

>The WSGI interface has two sides: the "server" or "gateway" side, and the "application" or "framework" side. The server side invokes a callable object that is provided by the application side.

pep333 定义了python web框架和web server之间的接口，只要框架实现了wsgi 接口，就可以被支持wsgi接口的web server调用。在这里，web server接收到请求，调用框架，获取输出。

如下是一个简单的满足wsgi 接口的python web应用：

```
def simple_app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']
```

web server预先定义start_response 方法供web 应用调用来收集输出，web server在调用web 应用时，同时传入environ变量来代表os当前的环境，server环境和web request。

具体在当前的gunicorn、flask环境下。
flask 在Flask对象里，通过__call__方法满足了wsgi的接口要求。

```
def __call__(self, environ, start_response):
        """The WSGI server calls the Flask application object as the
        WSGI application. This calls :meth:`wsgi_app` which can be
        wrapped to applying middleware."""
        return self.wsgi_app(environ, start_response)
```

gunicorn充当了web server，在相关的worker 对象里，通过语句`respiter = self.wsgi(environ, resp.start_response)`调用了应用框架。


# gunicorn

* master/pre-fork worker
* worker class
  * sync
    * default
  * coroutine
    * eventlet
    * gevent
  * asyncio
    * tornado
  * threads
    * gthread
* wsgi

# Flask

>There is only one limiting factor regarding scaling in Flask which are the context local proxies. They depend on context which in Flask is defined as being either a thread, process or greenlet. If your server uses some kind of concurrency that is not based on threads or greenlets, Flask will no longer be able to support these global proxies. 

## overview

* most based on Werkzeug && jinja2
* rich hook and signal

## how flask handler a request
![request-in-flask](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/request-in-flask.png)

## hook

### when before_first_request

Flask 是框架，对运行不做假设，框架的运行细节交给web server。比如gunicorn 可以通过基于线程的方式来调用app，也可以通过协程的方式来调用，当然还有同步的方式调用，再加上多进程。这里 before_first_request 所说的只是当前app 实例里的第一个请求。若guniciron 启动了多个进程，则多个进程会有多个 before_first_request。

```
def try_trigger_before_first_request_functions(self):
        """Called before each request and will ensure that it triggers
        the :attr:`before_first_request_funcs` and only exactly once per
        application instance (which means process usually).

        :internal:
        """
        if self._got_first_request:
            return
        with self._before_request_lock:
            if self._got_first_request:
                return
            for func in self.before_first_request_funcs:
                func()
            self._got_first_request = True
```

`_before_request_lock` 是一个theading.Lock 对象，保证了进程内部的同步。

## other hook

## local proxy

[werkzeug.local.Local] (https://werkzeug.palletsprojects.com/en/master/local/) 建造了一个以greenlet.getcurrent()/thread.get_ident() 返回id为key的 两层dict数据结构，各自context下的变量存在对应的key下。相对于threading.local()，werkzeug.local.Local 额外实现了greenlet独立。<i>The same context means the same greenlet (if you’re using greenlets) in the same thread and same process.</i>

werkzeug 同时通过了local proxy机制，将操作传递给背后的local 变量。使得同样的变量名在不同的context 下可以访问不同的内容。

Flask 提供了`current_app, g, request, session` 四个localproxy对象。在一个请求内，任何方法可以方便的访问这些变量，这些变量对于其他请求是独立存在。

```
class Local(object):
    __slots__ = ("__storage__", "__ident_func__")

    def __init__(self):
        object.__setattr__(self, "__storage__", {})
        object.__setattr__(self, "__ident_func__", get_ident)

    def __iter__(self):
        return iter(self.__storage__.items())

    def __call__(self, proxy):
        """Create a proxy for a name."""
        return LocalProxy(self, proxy)

    def __release_local__(self):
        self.__storage__.pop(self.__ident_func__(), None)

    def __getattr__(self, name):
        try:
            return self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        ident = self.__ident_func__()
        storage = self.__storage__
        try:
            storage[ident][name] = value
        except KeyError:
            storage[ident] = {name: value}

    def __delattr__(self, name):
        try:
            del self.__storage__[self.__ident_func__()][name]
        except KeyError:
            raise AttributeError(name)
```

