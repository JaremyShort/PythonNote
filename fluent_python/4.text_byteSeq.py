import os
import struct

"""
• 字符、码位和字节表述
• bytes、bytearray 和 memoryview 等二进制序列的独特特性
• 全部 Unicode 和陈旧字符集的编解码器
• 避免和处理编码错误
• 处理文本文件的最佳实践
• 默认编码的陷阱和标准 I/O 的问题
• 规范化 Unicode 文本，进行安全的比较
• 规范化、大小写折叠和暴力移除音调符号的实用函数
• 使用 locale 模块和 PyUCA 库正确地排序 Unicode 文本
• Unicode 数据库中的字符元数据
• 能处理字符串和字节序列的双模式 API
"""

print("--------------------------------------字符问题--------------------------------------")
# bytes不可变类型    bytearray可变类型

# 编码和解码
s = 'café'
print(len(s))
b = s.encode('utf8')
print(b)
print(len(b))
b = b.decode('utf8')
print(b)

cafe = bytes(s, encoding='utf_8')
print(cafe)
print(cafe[0])
print(cafe[:1])

cafe_arr = bytearray(cafe)
print(cafe_arr)
print(cafe_arr[-1:])

# bytes[0]获取的是一个整数，而bytes[:1]返回的是一个长度为 1 的bytes对象。s[0] == s[:1] 只对 str 这个序列类型成立。
print(cafe[0] == cafe[:1])
print(cafe_arr[0] == cafe_arr[:1])
print(s[0] == s[:1])

print("--------------------------------------结构体和内存视图--------------------------------------")

# 结构体 struct / 内存试图 memoryview
fmt = '<3s3sHH'  # 结构体的格式：< 是小字节序，3s3s 是两个 3 字节序列，HH 是两个 16 位二进制整数。
with open('test.png', 'rb') as fp:
    img = memoryview(fp.read())  # 使用内存中的文件内容创建一个 memoryview 对象
header = img[:10]  # 使用切片再创建一个 memoryview 对象；这里不会复制字节序列。
print(bytes(header))
print(struct.unpack(fmt, header))  # 拆包 memoryview 对象，得到一个元组，包含类型、版本、宽度和高度。
del header
del img

print("--------------------------------------基本的编解码器--------------------------------------")
for codec in ['latin_1', 'utf_8', 'utf_16']:
    print(codec, 'El Niño'.encode(codec), sep='\t')

"""
典型编码：
latin1（即 iso8859_1）
一种重要的编码，是其他编码的基础，例如 cp1252 和 Unicode（注意，latin1 与 cp1252 的字节值是一样的，甚至连码位也相同）。
cp1252
Microsoft 制定的 latin1 超集，添加了有用的符号，例如弯引号和€（欧元）；有些Windows 应用把它称为“ANSI”，但它并不是 ANSI 标准。
cp437
IBM PC 最初的字符集，包含框图符号。与后来出现的 latin1 不兼容。
gb2312
用于编码简体中文的陈旧标准；这是亚洲语言中使用较广泛的多字节编码之一。
utf-8
目前 Web 中最常见的 8 位编码；3 与 ASCII 兼容（纯 ASCII 文本是有效的 UTF-8 文本）。
utf-16le
UTF-16 的 16 位编码方案的一种形式；所有 UTF-16 支持通过转义序列（称为“代理对”，surrogate pair）表示超过 U+FFFF 的码位。
"""

print("---------------------------------------处理文本文件---------------------------------------")
# 编码侦测包 Chardet 用于识别编码类型

fp = open('cafe.txt', 'w', encoding='utf_8')
print(fp)
fp.write('café')
fp.close()
print(os.stat('cafe.txt').st_size)

fp2 = open('cafe.txt')
print(fp2)
print(fp2.encoding)
fp2.read()
fp3 = open('cafe.txt', encoding='utf_8')
print(fp3)
print(fp3.read())
fp4 = open('cafe.txt', 'rb')
print(fp4)
print(fp4.read())

print("--------------------------------------Unicode文本排序--------------------------------------")

import pyuca

# Unicode 排序算法库

coll = pyuca.Collator()
fruits = ['caju', 'atemoia', 'cajá', 'açaí', 'acerola']
sorted_fruits = sorted(fruits, key=coll.sort_key)
print(fruits)

s = "123456789"
print(s[len(s) - 3:])
