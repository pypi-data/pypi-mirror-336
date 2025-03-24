#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="huaxia-zhicheng-pmp-renzheng-kaoshi-yubei-kecheng-houlijun-fix1",
    version=HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1.__version__,
    url="https://github.com/apachecn/huaxia-zhicheng-pmp-renzheng-kaoshi-yubei-kecheng-houlijun-fix1",
    author=HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1.__author__,
    author_email=HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1.__email__,
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
    description="华夏智诚 PMP 认证考试预备课程（侯利军）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "huaxia-zhicheng-pmp-renzheng-kaoshi-yubei-kecheng-houlijun-fix1=HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1.__main__:main",
            "HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1=HuaxiaZhichengPmpRenzhengKaoshiYubeiKechengHoulijunFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
