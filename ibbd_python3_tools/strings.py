# -*- coding: utf-8 -*-
#
# 扩展的字符串处理函数
# Author: alex
# Created Time: 2018年06月13日 星期三 16时07分46秒


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
