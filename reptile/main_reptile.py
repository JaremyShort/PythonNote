# 爬虫

from urllib import request, parse

# resp = request.urlopen("http://github.com/")

# date = request.urlretrieve("http://github.com/", "github.html")


# # url 编码及解码
# data = {"name": "Jaremy", "age": 30, "greet": "你好"}
# qs = parse.urlencode(data)
# print(qs)
# data = parse.parse_qs(qs)
# print(data)

# # 字符串编码  
# parse.quote()


url = "https://www.baidu.com/s?wd=%E6%9E%97%E4%BF%8A%E6%9D%B0&rsv_spt=1&rsv_iqid=0xaeee165e00040469&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=ib&rsv_sug3=11&rsv_sug1=7&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=1660&rsv_sug4=9845"

# resp = request.urlopen(url)

# print(resp.read())


# url 解析  parse.urlparse  parse.urlsplit
result = parse.urlsplit(url)
print(result)