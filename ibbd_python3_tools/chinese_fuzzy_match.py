# -*- coding: utf-8 -*-
#
# 中文模糊匹配
# Author: alex
# Created Time: 2019年03月14日 星期四 09时54分14秒
import re
from enum import Enum
from pypinyin import lazy_pinyin


# 拼音的分隔符
py_space = "\\s|\\.|\\,|\\!|\\?|。|，|！|？"
# 模糊匹配配置
fuzzy_start = [
    ('sh', 'ch', 'zh'),
    ('s', 'c', 'z'),
]
fuzzy_end = [
    ('ang', 'eng', 'ing'),
    ('an', 'en', 'in'),
]


class MatchType(str, Enum):
    """匹配类型:
        full: 完整匹配
        pinyin: 拼音匹配
        fuzzy: 模糊拼音
        not_match: 没匹配上
    """
    Full = 'full'
    Pinyin = 'pinyin'
    Fuzzy = 'fuzzy'
    NotMatch = 'not_match'


def chinese_fuzzy_match(match_string, string, use_fuzzy=True):
    """中文模糊匹配，支持拼音，支持模糊拼音
    从string中匹配match_string
    支持的模糊音有：
    1. 声母模糊音：s <--> sh，c<-->ch，z <-->zh
    2. 韵母模糊音：an<-->ang，en<-->eng，in<-->ing
    Args:
        match_string: 需要匹配的字符串
        string: 被匹配的字符串
        use_fuzzy: 是否开启拼音的模糊匹配，默认开启
    Returns:
        match_type: str, 匹配类型:
            full: 完整匹配
            pinyin: 拼音匹配
            fuzzy: 模糊拼音
            not_match: 没匹配上
    Examples:
        string = '张三丰来了'
        match = '章叁风'
        print(chinese_fuzzy_match(match, string))
    """
    res = {   # 返回格式
        'match_type': MatchType.NotMatch.value
    }
    # 完整匹配
    if match_string in string:
        res['match_type'] = MatchType.Full.value
        return res

    # 拼音匹配
    str_ls = lazy_pinyin(string)
    match_ls = lazy_pinyin(match_string)
    if py_full_math(match_ls, str_ls):
        res['match_type'] = MatchType.Pinyin.value
        return res

    if use_fuzzy:
        # 拼音模糊匹配
        f_str_ls = py_fuzzy_format(str_ls)
        f_match_ls = py_fuzzy_format(match_ls)
        if py_full_math(f_match_ls, f_str_ls):
            res['match_type'] = MatchType.Fuzzy.value
            return res

    return res


def py_full_math(match_ls, str_ls):
    """拼音字符串是否匹配"""
    str_py = ' '.join(str_ls)
    match_py = ' '.join(match_ls)
    print(match_py, str_py)
    if re.findall("(^|{start}){match}($|{end})".format(
        start=py_space,
        match=match_py,
        end=py_space,
    ), str_py):
        return True
    return False


def py_fuzzy_format(py_ls):
    """格式化模糊拼音"""
    new_py_ls = []
    # 开始匹配
    for word in py_ls:
        # 前缀匹配
        match_word = None
        for match, rep in zip(fuzzy_start[0], fuzzy_start[1]):
            if word.startswith(match):
                match_word = (match, rep)
                break
        if match_word:
            word = match_word[1] + word[len(match_word[0]):]

        # 后缀匹配
        match_word = None
        for match, rep in zip(fuzzy_end[0], fuzzy_end[1]):
            if word.endswith(match):
                match_word = (match, rep)
                break
        if match_word:
            word = word[:-len(match_word[0])] + match_word[1]

        new_py_ls.append(word)

    return new_py_ls


if __name__ == '__main__':
    print('测试拼音完整匹配：')
    match = 'zhang san feng'
    string = 'zhang san feng lai le'
    print("%s ==> %s: True == %s" %
          (match, string, py_full_math(match.split(' '), string.split(' '))))
    string = 'wo zhang san feng lai le'
    print("%s ==> %s: True == %s" %
          (match, string, py_full_math(match.split(' '), string.split(' '))))
    string = 'wo zhang san feng'
    print("%s ==> %s: True == %s" %
          (match, string, py_full_math(match.split(' '), string.split(' '))))
    string = 'wo zhang san fen'
    print("%s ==> %s: False == %s" %
          (match, string, py_full_math(match.split(' '), string.split(' '))))

    print("\n\n拼音模糊格式化：")
    string = 'zhang shan fen lai'
    match = 'zan san fen lai'
    f_str = py_fuzzy_format(string.split(' '))
    print("%s == %s: %s" %
          (string, ' '.join(f_str), match == ' '.join(f_str)))

    print("\n\n中文匹配：")
    string = '张三丰来了'
    match = '章叁风'
    print("%s ==> %s" % (match, string))
    print(chinese_fuzzy_match(match, string))
    string = '张三丰来了'
    match = '占山芬'
    print("%s ==> %s" % (match, string))
    print(chinese_fuzzy_match(match, string))
    string = '张三丰来了'
    match = '占山芬'
    print("%s ==> %s" % (match, string))
    print('not_match: ', chinese_fuzzy_match(match, string, use_fuzzy=False))
    match = '李四'
    print("%s ==> %s" % (match, string))
    print(chinese_fuzzy_match(match, string))
