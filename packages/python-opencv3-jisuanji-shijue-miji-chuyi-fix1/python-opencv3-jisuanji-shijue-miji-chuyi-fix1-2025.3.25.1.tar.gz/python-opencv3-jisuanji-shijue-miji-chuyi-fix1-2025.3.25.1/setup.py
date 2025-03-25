#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import PythonOpencv3JisuanjiShijueMijiChuyiFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('PythonOpencv3JisuanjiShijueMijiChuyiFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="python-opencv3-jisuanji-shijue-miji-chuyi-fix1",
    version=PythonOpencv3JisuanjiShijueMijiChuyiFix1.__version__,
    url="https://github.com/apachecn/python-opencv3-jisuanji-shijue-miji-chuyi-fix1",
    author=PythonOpencv3JisuanjiShijueMijiChuyiFix1.__author__,
    author_email=PythonOpencv3JisuanjiShijueMijiChuyiFix1.__email__,
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
    description="Python OpenCV3 计算机视觉秘籍（初译）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "python-opencv3-jisuanji-shijue-miji-chuyi-fix1=PythonOpencv3JisuanjiShijueMijiChuyiFix1.__main__:main",
            "PythonOpencv3JisuanjiShijueMijiChuyiFix1=PythonOpencv3JisuanjiShijueMijiChuyiFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
