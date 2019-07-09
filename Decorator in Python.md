# Decorator in Python

>A decorator is a callable that takes another function as argument (the decorated function).The decorator may perform some processing with the decorated function, and returns it or replaces it with another function or callable object.

这里有一个输入，一个输出。输入是原function，输出是一个callable 对象，可以是原function，也可以是新的。

## decorator without args

```
def deco(f):

    @functions.wraps(f)
    def inner():
        return f()      # add retutn to return the value from call f()
    
    return inner


@deco
def foo():
    pass
```

syntax sugar for decorator: @. 上述行为等于: `foo = deco(foo)`

如果是多层decorator，执行顺序将是一个递归的执行顺序，最上面的先进入。

![deco-on-deco](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/deco-on-deco.png)


## closure
![closure-in-python](https://liwb-csdn.oss-cn-hangzhou.aliyuncs.com/closure-in-python.png)

>a closure is a function with an extended scope that encompasses nonglobal variables referenced in the body of the function but not defined there. it can access nonglobal variables that are defined outside of its body.

>The first and simplest answer is “dynamic scope.” This means that free variables are evaluated by looking into the envi‐ ronment where the function is invoked.

>Today, lexical scope is the norm: free variables are evaluated considering the environ‐ ment where the function is defined. Lexical scope complicates the implementation of languages with first-class functions, because it requires the support of closures.

闭包，我的理解是一个特性。它隐藏了一些变量，这些变量只有某些函数才可以访问，相当于一些变量被包进去了，而原来拥有它的对象可能已经消失了。
有了闭包机制，inner方法里才可以记住传入的f函数，以及在deco可能会定义的其他变量。

往往我们可以通过实现class 的__call__方法来代替一个闭包。比如图中的闭包，我们可以定义如下class

```
class Average():
    def __init__(self, series):
        self.series = list(series)

    def __call__(selft, new_value):
        self.series.append(new_value)
        total = sum(series)
        return total/len(series)

averager = Average([])
```

## decorator with args

带参数的decorator需要包裹一层。

```
@deco(v)
def foo():
    pass
```

deco的实现如下：

```
def deco(v):
    def real_deco(f):
        def inner():
            f()
        return inner
    
    return real_deco
```

即是说@ 后面的函数先执行生成真正的decorator，随后应用到原函数上。


## functions.wraps 的作用

先说patrial。partial 实际上是一个实现了__call__ 的类。partial 的作用是固定function的参数。固定的参数存在self.args、self.keywords 里了。

```
    def __call__(*args, **keywords):
        if not args:
            raise TypeError("descriptor '__call__' of partial needs an argument")
        self, *args = args
        newkeywords = self.keywords.copy()
        newkeywords.update(keywords)
        return self.func(*self.args, *args, **newkeywords)
```

按照`decorator with args` 介绍的流程。`@functions.wraps(f)` wraps 是一个factory function，生成真正的decorator。可以看到wraps 是调用了update_wrapper 函数，利用partial 固定了一些参数，只剩下wrapper 参数。这个参数在应用@ 的时候，会传入将要decorator的函数，就是这里的 inner。在update_wrapper 里，会对wrapped 的属性进行一些修改。

说白了，functions.wraps 的作用就是让decorator 函数看起来和decorated 函数一样。

```
def wraps(wrapped,
          assigned = WRAPPER_ASSIGNMENTS,
          updated = WRAPPER_UPDATES):
    """Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """
    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)                   
```

```
def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper
```

