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

# region namedtuple

from collections import namedtuple

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
