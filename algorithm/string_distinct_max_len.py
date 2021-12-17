def lengthOfLongestSubstring(s: str) -> int:

    return func1(s)


def func1(s: str):
    length = 0
    if s:
        max_length = len(s)
        if max_length == 1:
            length == max_length
        for i in range(max_length):
            for j in range(max_length + 1):
                if j > i:
                    new_str = s[i:j]
                elif i == j:
                    new_str = s
                has_repeat = False
                for k in new_str:
                    if new_str.count(k) > 1:
                        has_repeat = True
                        break
                if not has_repeat and len(new_str) > length:
                    length = len(new_str)
    return length


# def func2(s: str):

#     # abceabcabc
#     length = 0
#     max_length = len(s)

#     key_length = {}  # 第几位/长度
#     key_pos = {}  # 字符出现的位置
#     max_not_repeat_index = 0
#     for i in range(max_length):
#         key_length.update({i: 0})

#         if s[i] in keys:
#             if max_not_repeat_index == 0 or i < max_not_repeat_index:
#                 # 中间有重复字段
#                 max_not_repeat_index = i
#                 length = max_not_repeat_index - s[i]
#             else:

#                 pass

#     return length
