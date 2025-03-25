#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import JavaMianshiBiwenJvmKaodianJingjiangFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('JavaMianshiBiwenJvmKaodianJingjiangFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="java-mianshi-biwen-jvm-kaodian-jingjiang-fix1",
    version=JavaMianshiBiwenJvmKaodianJingjiangFix1.__version__,
    url="https://github.com/apachecn/java-mianshi-biwen-jvm-kaodian-jingjiang-fix1",
    author=JavaMianshiBiwenJvmKaodianJingjiangFix1.__author__,
    author_email=JavaMianshiBiwenJvmKaodianJingjiangFix1.__email__,
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
    description="Java面试必问—JVM考点精讲 ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "java-mianshi-biwen-jvm-kaodian-jingjiang-fix1=JavaMianshiBiwenJvmKaodianJingjiangFix1.__main__:main",
            "JavaMianshiBiwenJvmKaodianJingjiangFix1=JavaMianshiBiwenJvmKaodianJingjiangFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
