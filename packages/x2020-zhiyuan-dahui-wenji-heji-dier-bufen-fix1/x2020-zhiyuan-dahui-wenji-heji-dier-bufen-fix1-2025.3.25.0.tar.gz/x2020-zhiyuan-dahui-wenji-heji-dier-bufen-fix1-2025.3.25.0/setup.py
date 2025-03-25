#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import X2020ZhiyuanDahuiWenjiHejiDierBufenFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('X2020ZhiyuanDahuiWenjiHejiDierBufenFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="x2020-zhiyuan-dahui-wenji-heji-dier-bufen-fix1",
    version=X2020ZhiyuanDahuiWenjiHejiDierBufenFix1.__version__,
    url="https://github.com/apachecn/x2020-zhiyuan-dahui-wenji-heji-dier-bufen-fix1",
    author=X2020ZhiyuanDahuiWenjiHejiDierBufenFix1.__author__,
    author_email=X2020ZhiyuanDahuiWenjiHejiDierBufenFix1.__email__,
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
    description="2020智源大会文集合集（第二部分）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "x2020-zhiyuan-dahui-wenji-heji-dier-bufen-fix1=X2020ZhiyuanDahuiWenjiHejiDierBufenFix1.__main__:main",
            "X2020ZhiyuanDahuiWenjiHejiDierBufenFix1=X2020ZhiyuanDahuiWenjiHejiDierBufenFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
