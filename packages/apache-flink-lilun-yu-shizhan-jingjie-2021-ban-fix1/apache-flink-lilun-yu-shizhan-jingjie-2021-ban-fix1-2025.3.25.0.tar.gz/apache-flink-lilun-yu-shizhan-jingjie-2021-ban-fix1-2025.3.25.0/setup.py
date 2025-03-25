#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ApacheFlinkLilunYuShizhanJingjie2021BanFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ApacheFlinkLilunYuShizhanJingjie2021BanFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="apache-flink-lilun-yu-shizhan-jingjie-2021-ban-fix1",
    version=ApacheFlinkLilunYuShizhanJingjie2021BanFix1.__version__,
    url="https://github.com/apachecn/apache-flink-lilun-yu-shizhan-jingjie-2021-ban-fix1",
    author=ApacheFlinkLilunYuShizhanJingjie2021BanFix1.__author__,
    author_email=ApacheFlinkLilunYuShizhanJingjie2021BanFix1.__email__,
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
    description="Apache Flink 理论与实战精解 2021 版",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "apache-flink-lilun-yu-shizhan-jingjie-2021-ban-fix1=ApacheFlinkLilunYuShizhanJingjie2021BanFix1.__main__:main",
            "ApacheFlinkLilunYuShizhanJingjie2021BanFix1=ApacheFlinkLilunYuShizhanJingjie2021BanFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
