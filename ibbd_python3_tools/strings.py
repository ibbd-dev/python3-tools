# -*- coding: utf-8 -*-
#
# 扩展的字符串处理函数
# Author: alex
# Created Time: 2018年06月13日 星期三 16时07分46秒
from settings import arabic_num_map


def conv_q2b(ustring):
    """全角转半角"""
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            if inside_code == 12288:  # 全角空格直接转换
                inside_code = 32
            elif inside_code >= 65281 and inside_code <= 65374:
                # 全角字符（除空格）根据关系转化
                inside_code -= 65248

            rstring += chr(inside_code)

        ss.append(rstring)

    return ''.join(ss)


def conv_single_arabic2chs(string):
    """将字符串中单一的阿拉伯数字转化为中文数字"""
    new_str = []
    slen = len(string)
    for i, c in zip(range(slen), string):
        is_single_arabic = False
        if c in arabic_num_map:
            is_single_arabic = True
            if i > 0 and string[i-1] in arabic_num_map:
                is_single_arabic = False  # 前一个字符不为数字

            if i < slen-1 and string[i+1] in arabic_num_map:
                is_single_arabic = False  # 后一个字符不为数字

        if is_single_arabic:
            new_str.append(arabic_num_map[c])
        else:
            new_str.append(c)

    return ''.join(new_str)


if __name__ == '__main__':
    arabic2chs = {
        '半岛1号': '半岛一号',
        '半岛10号': '半岛10号',
        '半岛5号': '半岛五号',
    }
    for k, v in arabic2chs.items():
        nk = conv_single_arabic2chs(k)
        if nk != v:
            raise Exception("conv single arabic2chs, key: %s, val: %s, new: %s" % (k, v, nk))
