# python3-tools
python3工具包

## install 

```sh
# 源码安装
python3 setup.py install

# 使用pip安装
pip3 install git+https://github.com/ibbd-dev/python3-tools
```

## 功能

- strings: 扩展的字符串模块
  - conv_q2b: 全角字符转化为半角字符
  - conv_single_arabic2chs: 将字符串中的单个阿拉伯数字转化为中文数字
- conv_chinese_digits_to_arabic: 中文数字转化为阿拉伯数字
- chinese_fuzzy_match: 中文模糊匹配，支持模糊拼音

