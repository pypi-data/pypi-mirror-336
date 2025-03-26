# -*- coding: utf-8 -*-
#===================================================================================================
#---    copyright 2017~2025, OBCon Inc.
#---    author gye hyun james kim <pnuskgh@gmail.com>
#---    license GNU GENERAL PUBLIC LICENSE v3.0 (https://github.com/jopenbusiness/StockHub?tab=GPL-3.0-1-ov-file)
#===================================================================================================

from setuptools import setup, find_packages

version = '0.0.1'

#--- PYPI (Python Package Index)
#---     https://pypi.org/
# https://velog.io/@rhee519/python-project-packaging-setuptools
setup(
    name='stockhub',
    version=version,
    author='gye hyun james kim', 
    author_email='pnuskgh@gmail.com', 
    description="증권사 Open API Hub 서비스", 
    keywords=[
        "Stock",
        "REST",
        "Open API",
        "Hub"
    ],
    url="https://github.com/jopenbusiness/StockHub",

    packages=find_packages(
        include=[ 
            'stockhub' 
        ],
        exclude=[]
    ),
    package_data={},
    install_requires=[
    ],
    python_requires='>=3.6'
)
