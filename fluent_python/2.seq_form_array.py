"""
容器序列
list、tuple 和 collections.deque 这些序列能存放不同类型的数据。
扁平序列
str、bytes、bytearray、memoryview 和 array.array，这类序列只能容纳一种类型。
容器序列存放的是它们所包含的任意类型的对象的引用，而扁平序列里存放的是值而不是
引用。换句话说，扁平序列其实是一段连续的内存空间。由此可见扁平序列其实更加紧
凑，但是它里面只能存放诸如字符、字节和数值这种基础类型。
序列类型还能按照能否被修改来分类。
可变序列
list、bytearray、array.array、collections.deque 和 memoryview。
不可变序列
tuple、str 和 bytes。
"""

import sys
import numpy
import bisect
import random as r
from array import array
from collections import namedtuple, deque

# region tuple使用
print("----------------------------tuple使用----------------------------")

lax_coordinates = (33.9425, -118.408056)
city, year, pop, chg, area = ('Tokyo', 2003, 32450, 0.66, 8014)  # 元组拆包
traveler_ids = [('USA', '31195855'), ('BRA', 'CE342567'), ('ESP', 'XDA205856')]
for passport in sorted(traveler_ids):
    print('%s/%s' % passport)  # 元组拆包

for country, _ in traveler_ids:
    print(country)

# 用*来处理剩下的元素
a, b, *rest = range(5)
print(a, b, rest)

metro_areas = [
    ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
    ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
    ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
    ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
    ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
]
print('{:15} | {:^9} | {:^9}'.format('', 'lat.', 'long.'))
fmt = '{:15} | {:9.4f} | {:9.4f}'
for name, cc, pop, (latitude, longitude) in metro_areas:
    if longitude <= 0:
        print(fmt.format(name, latitude, longitude))

# endregion

# region namedtuple使用

print("----------------------------namedtuple使用----------------------------")

City = namedtuple('City', 'name country population coordinates')
tokyo = City('Tokyo', 'JP', 36.933, (35.689722, 139.691667))
print(tokyo)
print(tokyo.name)

LatLong = namedtuple('LatLong', 'lat long')
delhi_data = ('Delhi NCR', 'IN', 21.935, LatLong(28.613889, 77.208889))
delhi = City._make(delhi_data)
print(delhi)
print(delhi._asdict())

# endregion

# region 切片

# 为什么切片和区间会忽略最后一个元素
print("----------------------------切片----------------------------")
"""
在切片和区间操作里不包含区间范围的最后一个元素是 Python 的风格，这个习惯符合
Python、C 和其他语言里以 0 作为起始下标的传统。这样做带来的好处如下。

• 当只有最后一个位置信息时，我们也可以快速看出切片和区间里有几个元素：range(3)
序列构成的数组 ｜ 29
和 my_list[:3] 都返回 3 个元素。
• 当起止位置信息都可见时，我们可以快速计算出切片和区间的长度，用后一个数减去第
一个下标（stop - start）即可。
• 这样做也让我们可以利用任意一个下标来把序列分割成不重叠的两部分，只要写成 my_
list[:x] 和 my_list[x:] 就可以了。
"""

l = [10, 20, 30, 40, 50, 60]
print(l[:2])
print(l[2:])

# seq[start:stop:step]  只能作为索引或者下标用在 [] 中来返回一个切片对象
print("----------------------seq[start:stop:step]----------------------")
s = 'bicycle'
print(s[::3])
print(s[::-1])

# 给切片赋值
print("----------------------------给切片赋值----------------------------")
# 切片赋值右侧必须是可迭代对象，即便只有单独一个值，也要把它转换成可迭代的序列。  ★★★

l = list(range(10))
print(l)
l[2:5] = [20, 30]
print(l)
del l[5:7]
print(l)
l[3::2] = [11, 22]
print(l)

# endregion

# region 序列常用操作

print("----------------------------对序列使用+和*----------------------------")
l = [1, 2, 3]
print(l * 5)
print(5 * 'abcd')

# 注意列表中是引用类型的情况  ★★★ 错误：不能使用[[]] * 3的形式
# 正确的写法如下：
board = [['_'] * 3 for i in range(3)]
print(board)
board[1][2] = 'X'
print(board)

print("----------------------------序列的增量赋值----------------------------")
# +=调用__iadd__，如果没有实现则调用__add__(a = a + b)， *=类似
# 可变序列一般都实现了 __iadd__ 方法，不会重新生成对象。而不可变序列根本就不支持这个操作，将会重新生成对象，效率也会低一些。  ★★★
# str类型是一个例外  ★★★

l = [1, 2, 3]
print(id(l))
l *= 2
print(l, id(l))

t = (1, 2, 3)
print(id(t))
t *= 2
print(t, id(t))

print(""" ★★★ http://www.pythontutor.com 可以对Python运行原理进行可视化分析的工具 """)

print("----------------------------list.sort方法和内置函数sorted----------------------------")
# list.sort 方法会就地排序列表，也就是说不会把原列表复制一份。内置函数 sorted，它会新建一个列表作为返回值
fruits = ['grape', 'raspberry', 'apple', 'banana']
print(sorted(fruits))
print(sorted(fruits, reverse=True))
print(sorted(fruits, key=len, reverse=True))

print("----------------------------用bisect来管理已排序的序列----------------------------")
# bisect 模块包含两个主要函数，bisect 和 insort，两个函数都利用 二分查找算法 来在有序序列中查找或插入元素。


print("----------------------------利用bisect搜索----------------------------")

HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]

ROW_FMT = '{0:2d} @ {1:2d} {2}{0:<2d}'


def demo(bisect_fn):
    for needle in reversed(NEEDLES):
        position = bisect_fn(HAYSTACK, needle)  # 用特定的 bisect 函数来计算元素应该出现的位置
        offset = position * ' |'  # 利用该位置来算出需要几个分隔符号。
        print(ROW_FMT.format(needle, position, offset))  # 把元素和其应该出现的位置打印出来。


if __name__ == '__main__':

    if sys.argv[-1] == 'left':  # 根据命令上最后一个参数来选用 bisect 函数。
        bisect_fn = bisect.bisect_left
    else:
        bisect_fn = bisect.bisect
    print('DEMO:', bisect_fn.__name__)  # 把选定的函数在抬头打印出来。
    print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
    demo(bisect_fn)

print("----------------------------利用bisect.insort插入新元素----------------------------")

SIZE = 7
r.seed(1729)
my_list = []
for i in range(SIZE):
    new_item = r.randrange(SIZE * 2)
    bisect.insort(my_list, new_item)
    print('%2d ->' % new_item, my_list)

# endregion

# region 数组

# print("------------------------------数组------------------------------")

# # 要一个只包含数字的列表，那么 array.array 比 list 更高效。数组支持所有跟可变序列有关的操作，包括 .pop、.insert 和 .extend。另外，数组还提供从文件读取和存入文件的更快的方法
#
# floats = array('d', (random() for i in range(10 ** 7)))  # 利用一个可迭代对象来建立一个双精度浮点数组（类型码是 'd'），这里我们用的可迭代对象是一个生成器表达式。
# print(floats[-1])
# fp = open('floats.txt', 'wb')
# floats.tofile(fp)  # 把数组存入一个二进制文件里
# fp.close()
#
# floats2 = array('d')
# fp = open('floats.txt', 'rb')
# floats2.fromfile(fp, 10 ** 7)
# fp.close()
# print(floats2[-1])
# print(floats2 == floats)

# endregion

# region 内存试图(memoryview)

print("----------------------------内存试图----------------------------")

# memoryview 是一个内置类，是泛化和去数学化的 NumPy 数组，它能让用户在不复制内容的情况下操作同一个数组的不同切片。
# memoryview.cast 的概念跟数组模块类似，能用不同的方式读写同一块内存数据，而且内容字节不会随意移动。

numbers = array('h', [-2, -1, 0, 1, 2])
memv = memoryview(numbers)  # 利用含有 5 个短整型有符号整数的数组（类型码是 'h'）创建一个 memoryview
print(memv.tolist())  # memv 里的 5 个元素跟数组里的没有区别。

memv_oct = memv.cast('B')  # 创建一个 memv_oct，这一次是把 memv 里的内容转换成 'B' 类型，也就是无符号字符。
print(memv_oct.tolist())
memv_oct[5] = 4
print(memv_oct.tolist())
print(numbers)

# endregion

# region Numpy

print("------------------------------numpy.ndarray 行和列进行基本操作------------------------------")

a = numpy.arange(12)
print(a)
print(a.shape)
a.shape = 3, 4
print(a)
print(a[2])
print(a[2, 1])
print(a[:, 1])  # 第 1 列
print(a.transpose())  # 把行和列交换，就得到了一个新数组。

# endregion

# region 队列

print("------------------------------双向队列和其他形式的队列------------------------------")

dq = deque(range(10), maxlen=10)  # maxlen 是一个可选参数，代表这个队列可以容纳的元素的数量，而且一旦设定，这个属性就不能修改了。
print(dq)
dq.rotate(3)  # 队列的旋转操作接受一个参数 n，当 n > 0 时，队列的最右边的 n 个元素会被移动到队列的左边。当 n < 0 时，最左边的 n 个元素会被移动到右边。
print("rotate(3)")
print(dq)
dq.rotate(-4)
print("rotate(-4)")
print(dq)
dq.appendleft(-1)  # 当试图对一个已满（len(d) == d.maxlen）的队列做头部添加操作的时候，它尾部的元素会被删除掉。注意在下一行里，元素 0 被删除了。
print("appendleft(-1)")
print(dq)
dq.extend([11, 22, 33])  # 在尾部添加 3 个元素的操作会挤掉头部 -1、1 和 2。
print("extend([11, 22, 33])")
print(dq)
dq.extendleft([10, 20, 30, 40])  # extendleft(iter) 方法会把迭代器里的元素逐个添加到双向队列的左边，因此迭代器里的元素会逆序出现在队列里。
print("extendleft([10, 20, 30, 40])")
print(dq)

# ★★★ 双向队列从队列中间删除元素的操作会慢一些，因为它只对头尾的操作进行了优化 ★★★

# endregion
