#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import PycharmZhongwenZhinanFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('PycharmZhongwenZhinanFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="pycharm-zhongwen-zhinan-fix1",
    version=PycharmZhongwenZhinanFix1.__version__,
    url="https://github.com/apachecn/pycharm-zhongwen-zhinan-fix1",
    author=PycharmZhongwenZhinanFix1.__author__,
    author_email=PycharmZhongwenZhinanFix1.__email__,
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
    description="PyCharm 中文指南",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "pycharm-zhongwen-zhinan-fix1=PycharmZhongwenZhinanFix1.__main__:main",
            "PycharmZhongwenZhinanFix1=PycharmZhongwenZhinanFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
