# coding:utf-8

from setuptools import setup

setup(
    name="PipeGraphPy",
    description="核心算法框架",
    version="2.0.16",
    license="Private",
    include_package_data=True,
    install_requires=[
        "python-dateutil>=2.8.2",
        "prettytable==3.7.0",
        "pandas>=1.3.5",
        "joblib>=1.3.2",
        "dbpoolpy>=0.6.11",
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
    ],
)
