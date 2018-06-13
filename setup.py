# -*- coding: utf-8 -*-
#
# 安装程序
# Author: alex
# Created Time: 2018年04月02日 星期一 17时29分45秒
#from setuptools import setup
from distutils.core import setup


LONG_DESCRIPTION = """
Python常用的相关工具库
""".strip()

SHORT_DESCRIPTION = """
Python常用的相关工具库
""".strip()

DEPENDENCIES = [
]

VERSION = '0.5.0'
URL = 'https://github.com/ibbd-dev/python3-tools'

PACKAGE_NAME = 'ibbd_python3_tools'

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url=URL,

    author='Alex Cai',
    author_email='cyy0523xc@gmail.com',
    license='Apache Software License',

    keywords='python3 tools utils',

    packages=[PACKAGE_NAME],
)
