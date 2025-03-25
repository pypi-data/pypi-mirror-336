#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="zhongguo-qiye-2020-rengongzhineng-yingyong-shijian-yu-qushi-fix1",
    version=ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1.__version__,
    url="https://github.com/apachecn/zhongguo-qiye-2020-rengongzhineng-yingyong-shijian-yu-qushi-fix1",
    author=ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1.__author__,
    author_email=ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1.__email__,
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
    description="中国企业2020：人工智能应用实践与趋势",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "zhongguo-qiye-2020-rengongzhineng-yingyong-shijian-yu-qushi-fix1=ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1.__main__:main",
            "ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1=ZhongguoQiye2020RengongzhinengYingyongShijianYuQushiFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
