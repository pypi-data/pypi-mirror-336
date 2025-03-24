#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="niuke-kuaixiao-xingye-qiuzhi-gonglve-baiwei-pian-2021-2022-fix1",
    version=NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1.__version__,
    url="https://github.com/apachecn/niuke-kuaixiao-xingye-qiuzhi-gonglve-baiwei-pian-2021-2022-fix1",
    author=NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1.__author__,
    author_email=NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1.__email__,
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
    description="牛客快消行业求职攻略—百威篇 2021~2022",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "niuke-kuaixiao-xingye-qiuzhi-gonglve-baiwei-pian-2021-2022-fix1=NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1.__main__:main",
            "NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1=NiukeKuaixiaoXingyeQiuzhiGonglveBaiweiPian20212022Fix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
