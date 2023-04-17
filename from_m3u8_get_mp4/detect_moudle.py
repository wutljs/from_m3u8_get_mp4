# -*- coding: utf-8 -*-
# @Author  : LouJingshuo
# @E-mail  : 3480339804@qq.com
# @Time    : 2023/4/16 15:11
# @Function: Infringement must be investigated, please indicate the source of reproduction!
"""This module is used to download the package that the program depends on running,using Tsinghua source."""

import os

package_list = ['pycryptodome', 'aiohttp', 'aiofiles']

for package in package_list:
    os.system(f'pip install {package} -i https://pypi.tuna.tsinghua.edu.cn/simple')
