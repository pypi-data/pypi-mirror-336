#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="niuke-qichexingye-mingqi-bi-mianshi-xiaozhao-qiuzhi-gonglve-2021-2022-fix1",
    version=NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1.__version__,
    url="https://github.com/apachecn/niuke-qichexingye-mingqi-bi-mianshi-xiaozhao-qiuzhi-gonglve-2021-2022-fix1",
    author=NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1.__author__,
    author_email=NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Text Processing :: Markup :: Markdown",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Documentation",
        "Topic :: Documentation",
    ],
    description="牛客汽车行业名企笔面试校招求职攻略 2021~2022",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "niuke-qichexingye-mingqi-bi-mianshi-xiaozhao-qiuzhi-gonglve-2021-2022-fix1=NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1.__main__:main",
            "NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1=NiukeQichexingyeMingqiBiMianshiXiaozhaoQiuzhiGonglve20212022Fix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
