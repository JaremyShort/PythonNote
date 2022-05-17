import re
import sys
import builtins
from unicodedata import name
from types import MappingProxyType
from collections import abc, defaultdict, OrderedDict, ChainMap, Counter, UserDict

# region 泛映射类型
print("-------------------------------------泛映射类型-------------------------------------")

# 散列表则是字典类型性能出众的根本原因  ★★★

my_dict = {}
print(type(my_dict))
print(isinstance(my_dict, abc.Mapping))
# 这里用 isinstance 而不是 type 来检查某个参数是否为 dict 类型，因为这个参数有可能不是 dict，而是一个比较另类的映射类型

# ★★★★★★
# 标准库里的所有映射类型都是利用 dict 来实现的，因此它们有个共同的限制，即只有可散列的数据类型才能用作这些映射里的键（只有键有这个要求，值并不需要是可散列的数据类型）。
# 什么是可散列的数据类型：
#    如果一个对象是可散列的，那么在这个对象的生命周期中，它的散列值是不变的，而且这个对象需要实现 __hash__() 方法。
#    另外可散列对象还要有 __eq__()方法，这样才能跟其他键做比较。如果两个可散列对象是相等的，那么它们的散列值一定是一样的。
# 可散列类型：str、bytes、数值类型、frozenset，元组只有当一个元组包含的所有元素都是可散列类型的情况下，它才是可散列的。
# ★★★★★★

tt = (1, 2, (30, 40))
print(hash(tt))
# (1, 2, [30, 40]) list是可变类型 ★★★
tf = (1, 2, frozenset([30, 40]))
print(hash(tf))

# endregion

# region 字典
print("--------------------------------------创建字典--------------------------------------")

# 多种创建字典方式
a = dict(one=1, two=2, three=3)
b = {'one': 1, 'two': 2, 'three': 3}
c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
d = dict([('two', 2), ('one', 1), ('three', 3)])
e = dict({'three': 3, 'one': 1, 'two': 2})
print(a == b == c == d == e)

# 字典推导
print("--------------------------------------字典推导--------------------------------------")
DIAL_CODES = [
    (86, 'China'),
    (91, 'India'),
    (1, 'United States'),
    (62, 'Indonesia'),
    (55, 'Brazil'),
    (92, 'Pakistan'),
    (880, 'Bangladesh'),
    (234, 'Nigeria'),
    (7, 'Russia'),
    (81, 'Japan')
]
country_code = {country: code for code, country in DIAL_CODES}
print(country_code)

print("------------------------------用setdefault处理找不到的键------------------------------")
# 当字典 d[k] 不能找到正确的键的时候，Python 会抛出异常
# 可以用 d.get(k, default) 来代替 d[k],更新不存在的键效率低

WORD_RE = re.compile(r'\w+')
index = {}
with open(sys.argv[0], encoding='utf-8') as fp:
    for line_no, line in enumerate(fp, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)

            # occurrences = index.get(word, [])  # 提取 word 出现的情况，如果还没有它的记录，返回 []。
            # occurrences.append(location)  # 把单词新出现的位置添加到列表的后面。
            # index[word] = occurrences  # 把新的列表放回字典中，这又牵扯到一次查询操作。

            index.setdefault(word, []).append(location)  # 1次查询
            # 等价于
            #     if key not in my_dict:
            #         my_dict[key] = []
            #     my_dict[key].append(new_value)  3次查询

# sorted 函数的 key= 参数没有调用 str.upper，而是把这个方法的引用传递给 sorted 函数，这样在排序的时候，单词会被规范成统一格式。
for word in sorted(index, key=str.upper):
    print(word, index[word])

print("-----------------------------用defaultdict处理找不到的键-----------------------------")

# index = {} 替换成 index = collections.defaultdict(list)
print("index = {} 替换成 index = collections.defaultdict(list)")

print("--------------------------------特殊方法__missing__--------------------------------")


class StrKeyDict0(dict):

    def __missing__(self, key):
        if isinstance(key, str):  # 不校验则会无限递归
            raise KeyError(key)
        return self[str(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return key in self.keys() or str(key) in self.keys()


d = StrKeyDict0([('2', 'two'), ('4', 'four')])
print(d['2'])
print(d[4])
# print(d[1])

print("-------------------------------------字典的变种------------------------------------")
# collections.OrderedDict
# 这个类型在添加键的时候会保持顺序，因此键的迭代次序总是一致的。OrderedDict的 popitem 方法默认删除并返回的是字典里的最后一个元素，但是如果像 my_odict.
# popitem(last=False) 这样调用它，那么它删除并返回第一个被添加进去的元素。

# collections.ChainMap
# 该类型可以容纳数个不同的映射对象，然后在进行键查找操作的时候，这些对象会被当作一个整体被逐个查找，直到键被找到为止。
# 这个功能在给有嵌套作用域的语言做解释器的时候很有用，可以用一个映射对象来代表一个作用域的上下文。
# 询规则的代码片段：

baseline = {'music': 'bach', 'art': 'rembrandt'}
adjustments = {'art': 'van gogh', 'opera': 'carmen'}
data = list(ChainMap(adjustments, baseline))
print("ChainMap：", data)

# collections.Counter
# 这个映射类型会给键准备一个整数计数器。每次更新一个键的时候都会增加这个计数器。
# 所以这个类型可以用来给可散列表对象计数，或者是当成多重集来用——多重集合就是集合里的元素可以出现不止一次。
# Counter 实现了 + 和 - 运算符用来合并记录，还有像 most_common([n]) 这类很有用的方法。most_common([n]) 会按照次序返回映射里最常见的 n 个键和它们的计数
ct = Counter('abracadabra')
print(ct)
ct.update('aaaaazzz')
print(ct)
ct.most_common(2)
print(ct)

print("-------------------------------------子类化UserDict------------------------------------")


class StrKeyDict(UserDict):

    def __missing__(self, key):
        if isinstance(key, str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, key):
        return str(key) in self.data

    def __setitem__(self, key, item):
        self.data[str(key)] = item


print("-------------------------------------不可变映射类型------------------------------------")

d = {1: 'A'}
d_proxy = MappingProxyType(d)
print(d_proxy)
print(d_proxy[1])
d[2] = 'B'
print(d_proxy)

print("----------------------------------------集合论---------------------------------------")

# 空集声明为set() ★★★
# 集合声明{1, 2, 3} 比 set([1, 2, 3])更快且更易读
# Python 必须先从 set 这个名字来查询构造方法，然后新建一个列表，最后再把这个列表传入到构造方法里。但是如果是像 {1, 2, 3} 这样的字面量，Python 会利用一个专门的叫作 BUILD_SET 的字节码来创建集合。

# 中缀运算符 |合集 &交集 -差集
set_a = {1, 2, 3}
set_b = {2, 4, 6}
print(len(set_a | set_b))
print(len(set_a - set_b))

print(len(set_a & set_b))
print(len(set(set_a).intersection(set_b)))

print(frozenset({0, 1, 2, 3, 4, 5, 6, 7, 8, 9}))
set_c = {chr(i) for i in range(32, 256) if 'SIGN' in name(chr(i), '')}
print(set_c)

print("----------------------------------------散列表---------------------------------------")
# 散列表其实是一个稀疏数组（总是有空白元素的数组称为稀疏数组）。
print(hash(1))
print(hash(1.0))

# CPython中，如果有一个整型对象，而且它能被存进一个机器字中，那么它的散列值就是它本身的值。
# 字典中的散列表原理：★★★   内存开销巨大
# 一个可散列的对象必须满足以下要求。
#   (1) 支持 hash() 函数，并且通过 __hash__() 方法所得到的散列值是不变的。
#   (2) 支持通过 __eq__() 方法来检测相等性。
#   (3) 若 a == b 为真，则 hash(a) == hash(b) 也为真
# 为了获取 my_dict[search_key] 背后的值，Python 首先会调用 hash(search_key) 来计算search_key 的散列值，把这个值最低的几位数字当作偏移量，
# 在散列表里查找表元（具体取几位，得看当前散列表的大小）。若找到的表元是空的，则抛出 KeyError 异常。若不是空的，则表元里会有一对 found_key:found_value。
# 这时候 Python 会检验 search_key == found_key 是否为真，如果它们相等的话，就会返回 found_value。
# 如果 search_key 和 found_key 不匹配的话，这种情况称为散列冲突。


print("----------------------------------------结束----------------------------------------")

# endregion
