# encoding=utf-8


def test1():
    def choose_class(name):
        if name == 'foo':
            class Foo(object):
                pass
            return Foo
        elif name == 'bar':
            class Bar(object):
                pass
            return Bar
        return None
    a = choose_class('foo')
    print a


def test2():
    class Foo(object):
        bar = True

    def cls_method(self, *args, **kwargs):
        print 'in instance %s method' % (self, )
        return None

    # 和其他内置类一样，str是创建string的类，int是创建整形的类，
    # 而type就是创建类（类也是对象）的类.
    FooChild = type('Foo', (object, ), dict(bar=True, cls_method=cls_method))
    print FooChild.bar
    print FooChild.cls_method  # Unbound method

    fc_ins = FooChild()
    print fc_ins.cls_method  # Bound method
    fc_ins.cls_method()


def test3():
    u"""什么是元类？type就是python内建的元类. 当然你可以自己定义元类. """

    class Foo(object):
        pass

    class Bar(type):
        pass

    class FooChild(object):
        # 注意：这里的__metaclass__必须是元类，而不是普通的类
        # 也可以是function，但是必须是像type一样，接受三个参数
        __metaclass__ = Bar

    print type(FooChild)


def test4():
    def upper_attr(cls_name, parents_name, cls_attrs):
        attrs = ((name, value) for name, value in cls_attrs.items() if not name.startswith('__'))
        print attrs  # It is a generator
        upper_attrs = dict((name.upper(), value) for name, value in attrs)
        return type(cls_name, parents_name, upper_attrs)

    class Foo(object):
        bar = True
        __metaclass__ = upper_attr

    class MetaFoo(type):
        pass

    class ClsFoo(object):
        __metaclass__ = MetaFoo

    print hasattr(Foo, 'bar')
    print hasattr(Foo, 'BAR')
    print type(Foo)  # output: type. Because upper_attr function return type()

    print type(ClsFoo)  # output: MetaFoo. Because MetaFoo is a metaclass (inherit from type)


def test5():
    """Use the real class as metaclass."""
    class UpperAttrMetaCls(type):
        def __new__(cls, cls_name, parents_name, cls_attrs):
            attrs = ((name, value) for name, value in cls_attrs.items() if not name.startswith('__'))
            upper_attrs = dict((name.upper(), value) for name, value in attrs)
            #return type(cls_name, parents_name, upper_attrs)  # not real OOP
            #return type.__new__(cls, cls_name, parents_name, upper_attrs)
            return super(UpperAttrMetaCls, cls).__new__(cls, cls_name, parents_name, upper_attrs)

    class Foo(object):
        __metaclass__ = UpperAttrMetaCls
        bar = True

    assert type(Foo) == UpperAttrMetaCls
    assert hasattr(Foo, 'bar') is False
    assert hasattr(Foo, 'BAR') is True


def test6():
    u"""初始化类可以看做是调用元类的__call__方法
    可以这样想，普通类的对象可以通过括号的形式调用类的__call__方法
    而普通对象是类的实例，同样类是元类的实例，
    也就是说，类可以通过括号的形式调用元类的__call__方法。
    """

    class MetaCls(type):

        def __call__(cls, *args, **kwargs):
            raise TypeError('Can not instantiate directly')

    class Foo(object):

        __metaclass__ = MetaCls

        @staticmethod
        def foo_method(x):
            print 'in foo_method'
            return x

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


def test7():
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
    test5()
