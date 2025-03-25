#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import WeilaiShequShuzihuaCaozuoxitongBaipishuFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('WeilaiShequShuzihuaCaozuoxitongBaipishuFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="weilai-shequ-shuzihua-caozuoxitong-baipishu-fix1",
    version=WeilaiShequShuzihuaCaozuoxitongBaipishuFix1.__version__,
    url="https://github.com/apachecn/weilai-shequ-shuzihua-caozuoxitong-baipishu-fix1",
    author=WeilaiShequShuzihuaCaozuoxitongBaipishuFix1.__author__,
    author_email=WeilaiShequShuzihuaCaozuoxitongBaipishuFix1.__email__,
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
    description="未来社区数字化操作系统白皮书",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "weilai-shequ-shuzihua-caozuoxitong-baipishu-fix1=WeilaiShequShuzihuaCaozuoxitongBaipishuFix1.__main__:main",
            "WeilaiShequShuzihuaCaozuoxitongBaipishuFix1=WeilaiShequShuzihuaCaozuoxitongBaipishuFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
