import random
from inspect import signature

print("---------------------------------------把函数视作对象---------------------------------------")

"""
一等对象(一等函数)：
• 在运行时创建
• 能赋值给变量或数据结构中的元素
• 能作为参数传给函数
• 能作为函数的返回结果
"""


# 接受函数为参数，或者把函数作为结果返回的函数是高阶函数


def factorial(n):
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n - 1)


print(factorial(42))
print(factorial.__doc__)
print(type(factorial))

fact = factorial
print(fact)
print(fact(42))
print(list(map(fact, range(11))))

print("---------------------------------------高阶函数---------------------------------------")
# 高阶函数：sorted、map、filter、reduce、apply
print(list(map(fact, range(6))))
print([fact(n) for n in range(6)])
print(list(map(factorial, filter(lambda n: n % 2, range(6)))))
print([factorial(n) for n in range(6) if n % 2])

print("---------------------------------------匿名函数---------------------------------------")
"""
lambda 关键字在 Python 表达式内创建匿名函数。
然而，Python 简单的句法限制了 lambda 函数的定义体只能使用纯表达式。换句话说，
lambda 函数的定义体中不能赋值，也不能使用 while 和 try 等 Python 语句。
在参数列表中最适合使用匿名函数★★★
"""
fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
print(sorted(fruits, key=lambda word: word[::-1]))

print("---------------------------------------可调用对象---------------------------------------")
"""
除了用户定义的函数，调用运算符（即 ()）还可以应用到其他对象上。如果想判断对象能
否调用，可以使用内置的 callable() 函数。Python 数据模型文档列出了 7 种可调用对象：
①用户定义的函数
使用 def 语句或 lambda 表达式创建。
②内置函数
使用 C 语言（CPython）实现的函数，如 len 或 time.strftime。
③内置方法
使用 C 语言实现的方法，如 dict.get。
④方法
在类的定义体中定义的函数。
⑤类
调用类时会运行类的 __new__ 方法创建一个实例，然后运行 __init__ 方法，初始化实
例，最后把实例返回给调用方。因为 Python 没有 new 运算符，所以调用类相当于调用
函数。（通常，调用类会创建那个类的实例，不过覆盖 __new__ 方法的话，也可能出现
其他行为。）
⑥类的实例
如果类定义了 __call__ 方法，那么它的实例可以作为函数调用。
⑦生成器函数
使用 yield 关键字的函数或方法。调用生成器函数返回的是生成器对象。
"""

print("---------------------------------------用户定义的可调用类型---------------------------------------")


class BingoCage:

    def __init__(self, items):
        self._items = list(items)
        random.shuffle(self._items)

    def pick(self):
        try:
            return self._items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')

    # 实现方法 __call__，可调用
    def __call__(self):

        return self.pick()


print("---------------------------------------从定位参数到仅限关键字参数---------------------------------------")


def tag(name, *content, cls=None, **attrs):
    """生成一个或多个HTML标签"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                           for attr, value
                           in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                         (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)


print(tag('br'))
print(tag('p', 'hello'))
print(tag('p', 'hello', 'world'))
print(tag('p', 'hello', id=33))
print(tag('p', 'hello', 'world', cls='sidebar'))
print(tag(content='testing', name="img"))

my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
print(tag(**my_tag))

print("---------------------------------------获取关于参数的信息---------------------------------------")


def clip(text, text1=None, max_len: 'int > 0' = 80) -> str:  # 展示注解格式
    """
    在max_len前面或后面的第一个空格处截断文本
    """
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # 没找到空格
        end = len(text)
    return text[:end].rstrip()


print(clip.__defaults__)  # 默认参数值，从后向前对应
print(clip.__code__)
print(clip.__code__.co_varnames)  # 参数列表，包含局部变量
print(clip.__code__.co_argcount)  # 参数个数

sig = signature(clip)
print(sig)
for name, param in sig.parameters.items():
    print(param.kind, ':', name, '=', param.default)
print("-------------------------------------------------------------------------------------------")
sig = signature(tag)
my_tag = {'name': 'img', 'title': 'Sunset Boulevard', 'src': 'sunset.jpg', 'cls': 'framed'}
bound_args = sig.bind(**my_tag)
print(bound_args)
for name, value in bound_args.arguments.items():
    print(name, '=', value)
# del my_tag['name']
# bound_args = sig.bind(**my_tag)  此时调用 sig.bind(**my_tag)，抛出 TypeError，提示缺少 name 参数


print("------------------------------------------函数注解------------------------------------------")
print(clip.__annotations__)  # 参数注解
print(sig.return_annotation)
for param in sig.parameters.values():
    note = repr(param.annotation).ljust(13)
    print(note, ':', param.name, '=', param.default)


print("------------------------------------------支持函数式编程的包------------------------------------------")
