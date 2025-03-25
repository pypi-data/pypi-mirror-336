#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="niuke-2021-hulianwang-xiaozhao-kaigua-gonglve-chanpin-yunying-pian-fix1",
    version=Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1.__version__,
    url="https://github.com/apachecn/niuke-2021-hulianwang-xiaozhao-kaigua-gonglve-chanpin-yunying-pian-fix1",
    author=Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1.__author__,
    author_email=Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1.__email__,
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
    description="牛客 2021 互联网校招开挂攻略产品运营篇",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "niuke-2021-hulianwang-xiaozhao-kaigua-gonglve-chanpin-yunying-pian-fix1=Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1.__main__:main",
            "Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1=Niuke2021HulianwangXiaozhaoKaiguaGonglveChanpinYunyingPianFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
