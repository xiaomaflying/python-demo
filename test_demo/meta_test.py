# encoding=utf-8

class MetaCls(type):

    def __call__(cls, *args, **kwargs):
        raise TypeError('Can not instantiate directly')


class Foo(object):

    __metaclass__ = MetaCls

    @staticmethod
    def foo_method(x):
        print 'in foo_method'
        return x


def test1():
    u"""初始化类可以看做是调用元类的__call__方法
    可以这样想，普通类的对象可以通过括号的形式调用类的__call__方法
    而普通对象是类的实例，同样类是元类的实例，
    也就是说，类可以通过括号的形式调用元类的__call__方法。
    """

    class CommonCls(object):
        def __call__(self, *args, **kwargs):
            print "in CommonCls class __call__"
            print args, kwargs

    common_cls = CommonCls()
    common_cls(1, 2, a="a", b="b")

    assert Foo.foo_method(1) == 1
    try:
        Foo()
    except TypeError as e:
        print e.message
    else:
        print 'normal'


def test2():
    u"""在元类的场景下，验证__call__和__new__的执行顺序"""

    class Meta(type):
        def __new__(cls, cls_name, bases, attrs):
            print "in meta class __new__"
            return type.__new__(cls, cls_name, bases, attrs)

        def __call__(cls, *args, **kwargs):
            print "in meta class __call__"
            print args, kwargs
            print super(cls)
            return cls.__new__(cls, *args, **kwargs)

    class Foo(object):
        __metaclass__ = Meta

        def __init__(self, *args, **kwargs):
            print "in Foo __init__"
            pass

    foo = Foo(1, 2, a="a", b="b")
    print foo


if __name__ == "__main__":
    test2()
