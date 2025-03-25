#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import IbmDeveloperworksQuanbuJiaochengErFix1
import os
from os import path

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

for subdir, _, _ in os.walk('IbmDeveloperworksQuanbuJiaochengErFix1'):
    fname = path.join(subdir, '__init__.py')
    open(fname, 'a').close()
    
setuptools.setup(
    name="ibm-developerworks-quanbu-jiaocheng-er-fix1",
    version=IbmDeveloperworksQuanbuJiaochengErFix1.__version__,
    url="https://github.com/apachecn/ibm-developerworks-quanbu-jiaocheng-er-fix1",
    author=IbmDeveloperworksQuanbuJiaochengErFix1.__author__,
    author_email=IbmDeveloperworksQuanbuJiaochengErFix1.__email__,
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
    description="IBM DeveloperWorks 全部教程（二）",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[],
    install_requires=[],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            "ibm-developerworks-quanbu-jiaocheng-er-fix1=IbmDeveloperworksQuanbuJiaochengErFix1.__main__:main",
            "IbmDeveloperworksQuanbuJiaochengErFix1=IbmDeveloperworksQuanbuJiaochengErFix1.__main__:main",
        ],
    },
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
