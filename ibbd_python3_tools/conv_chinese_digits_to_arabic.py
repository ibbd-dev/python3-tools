# -*- coding: utf-8 -*-
#
# 将中文，大写，全角等转为半角阿拉伯数字
# Author: Alex
#

chs_arabic_map = {'零': 0, '一': 1, '二': 2, '三': 3, '四': 4,
                  '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                  '十': 10, '百': 100, '千': 10 ** 3, '万': 10 ** 4,
                  '〇': 0, '壹': 1, '贰': 2, '叁': 3, '肆': 4,
                  '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9,
                  '拾': 10, '佰': 100, '仟': 10 ** 3, '萬': 10 ** 4,
                  '亿': 10 ** 8, '億': 10 ** 8, '幺': 1,
                  '０': 0, '１': 1, '２': 2, '３': 3, '４': 4,
                  '５': 5, '６': 6, '７': 7, '８': 8, '９': 9}


def conv_chinese_digits_to_arabic(chinese_digits_str):
    """将中文数字字符串转化为阿拉伯数字的字符串"""
    new_str = []
    has_digit = False
    tmp, result, hnd_mln = 0, 0, 0
    max_len = len(chinese_digits_str)
    for index, curr_char in zip(range(max_len), chinese_digits_str):
        curr_digit = chs_arabic_map.get(curr_char, None)
        if curr_digit is None:
            if has_digit:   # 把前面的数字加入字符串
                new_str.append(str(result+tmp+hnd_mln))
                has_digit = False
                tmp, result, hnd_mln = 0, 0, 0

            new_str.append(curr_char)
            continue

        has_digit = True
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            if tmp == 0 and hnd_mln == 0 and result == 0:   # 如果前面没有数字的话，则不能计算，例如：亿名
                has_digit = False
                new_str.append(curr_char)
                continue

            result = result + tmp
            result = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result = 0
            tmp = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            if tmp == 0 and hnd_mln == 0 and result == 0:   # 如果前面没有数字的话，则不能计算，例如：亿名
                has_digit = False
                new_str.append(curr_char)
                continue

            result = result + tmp
            result = result * curr_digit
            tmp = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            if tmp == 0 and hnd_mln == 0 and result == 0:   # 如果前面没有数字的话，则不能计算，例如：亿名
                # 前面没有数字相关的
                if curr_char != '十':
                    has_digit = False
                    new_str.append(curr_char)
                    continue
                elif index < max_len - 1 and chs_arabic_map.get(chinese_digits_str[index+1], None) is None:
                    # 当前字符不是最后一个，且下一个字符不是数字相关的
                    has_digit = False
                    new_str.append(curr_char)
                    continue

            tmp = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result

    if has_digit:   # 把前面的数字加入字符串
        new_str.append(str(result+tmp+hnd_mln))
        has_digit = False

    return ''.join(new_str)


if __name__ == "__main__":
    test_map = {
        '三千五百二十三': 3523,
        '七十五亿八百零七万九千二百零八': 7508079208,
        '四万三千五百二十一': 43521,
        '三千五百二十一': 3521,
        '三千五百零八': 3508,
        '三五六零': 3560,
        '一万零三十': 10030,
        '': '',
        #1 digit 个
        '零': 0,
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        #2 digits 十
        '十': 10,
        '十一': 11,
        '二十': 20,
        '二十一': 21,
        #3 digits 百
        '一百': 100,
        '一百零一': 101,
        '一百一十': 110,
        '一百二十三': 123,
        #4 digits 千
        '一千': 1000,
        '一千零一': 1001,
        '一千零一十': 1010,
        '一千一百': 1100,
        '一千零二十三': 1023,
        '一千二百零三': 1203,
        '一千二百三十': 1230,
        #5 digits 万
        '一万': 10000,
        '一万零一': 10001,
        '一万零一十': 10010,
        '一万零一百': 10100,
        '一万一千': 11000,
        '一万零一十一': 10011,
        '一万零一百零一': 10101,
        '一万一千零一': 11001,
        '一万零一百一十': 10110,
        '一万一千零一十': 11010,
        '一万一千一百': 11100,
        '一万一千一百一十': 11110,
        '一万一千一百零一': 11101,
        '一万一千零一十一': 11011,
        '一万零一百一十一': 10111,
        '一万一千一百一十一': 11111,
        #6 digits 十万
        '十万零二千三百四十五': 102345,
        '十二万三千四百五十六': 123456,
        '十万零三百五十六': 100356,
        '十万零三千六百零九': 103609,
        #7 digits 百万
        '一百二十三万四千五百六十七': 1234567,
        '一百零一万零一百零一': 1010101,
        '一百万零一': 1000001,
        #8 digits 千万
        '一千一百二十三万四千五百六十七': 11234567,
        '一千零一十一万零一百零一': 10110101,
        '一千万零一': 10000001,
        #9 digits 亿
        '一亿一千一百二十三万四千五百六十七': 111234567,
        '一亿零一百零一万零一百零一': 101010101,
        '一亿零一': 100000001,
        #10 digits 十亿
        '十一亿一千一百二十三万四千五百六十七': 1111234567,
        #11 digits 百亿
        '一百一十一亿一千一百二十三万四千五百六十七': 11111234567,
        #12 digits 千亿
        '一千一百一十一亿一千一百二十三万四千五百六十七': 111111234567,
        #13 digits 万亿
        '一万一千一百一十一亿一千一百二十三万四千五百六十七': 1111111234567,
        #14 digits 十万亿
        '十一万一千一百一十一亿一千一百二十三万四千五百六十七': 11111111234567,
        #17 digits 亿亿
        '一亿一千一百一十一万一千一百一十一亿一千一百二十三万四千五百六十七': 11111111111234567,
        'hah': 'hah',
        '一百哈哈': '100哈哈',
        '江北二十一号小区': '江北21号小区',
        '江北二十一号小区三十号': '江北21号小区30号',
        '万科帝景苑': '万科帝景苑',
        '中山万科帝景苑': '中山万科帝景苑',
        '回亿': '回亿',
        '十里银滩': '十里银滩',
        '1至２楼': '1至2楼',
        '大亚湾澳头四洲蜜方': '大亚湾澳头四洲蜜方',
    }

    for key, val in test_map.items():
        val = str(val)
        new_val = conv_chinese_digits_to_arabic(key)
        if new_val == val:
            pass
            #print("== %s %s" % (val, new_val))
        else:
            print("!! %s %s" % (val, new_val))
