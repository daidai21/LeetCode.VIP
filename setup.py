#!/usr/bin/env python3
# -*- coding:utf-8 -*-


# =============================================================================
# File Name: setup.py
# Author: DaiDai
# Mail: daidai4269@aliyun.com
# Created Time: Thu Aug 15 17:50:36 2019
# =============================================================================


from setuptools import setup
from setuptools import find_packages
import setuptools


install_requires = []
with open("requirements.txt") as f:
    for line in f.readlines():
        install_requires.append(line.rstrip("\n"))


setup(
    name="LeetCode.VIP",
    version="0.1",
    license = "",
    author='DaiDai',
    author_email='daidai4269@aliyun.com',
    long_description = "",
    description = "This is a simple shell tool about algorithms problem \
        information of LeetCode. This tool support linux and Mac OX.",
    url='https://github.com/daidai21/LeetCode.VIP',
    install_requires = install_requires,
)
