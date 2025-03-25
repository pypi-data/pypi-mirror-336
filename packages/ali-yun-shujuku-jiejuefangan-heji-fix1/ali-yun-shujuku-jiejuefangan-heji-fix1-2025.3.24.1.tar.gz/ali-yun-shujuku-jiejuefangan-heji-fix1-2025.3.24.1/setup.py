#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import AliYunShujukuJiejuefanganHejiFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('AliYunShujukuJiejuefanganHejiFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="ali-yun-shujuku-jiejuefangan-heji-fix1",
    version=AliYunShujukuJiejuefanganHejiFix1.__version__,
    url="https://github.com/apachecn/ali-yun-shujuku-jiejuefangan-heji-fix1",
    author=AliYunShujukuJiejuefanganHejiFix1.__author__,
    author_email=AliYunShujukuJiejuefanganHejiFix1.__email__,
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
    description="阿里云数据库解决方案合集",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "ali-yun-shujuku-jiejuefangan-heji-fix1=AliYunShujukuJiejuefanganHejiFix1.__main__:main",
            "AliYunShujukuJiejuefanganHejiFix1=AliYunShujukuJiejuefanganHejiFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
