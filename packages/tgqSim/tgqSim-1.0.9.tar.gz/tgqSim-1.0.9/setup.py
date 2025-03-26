"""
-*- coding: utf-8 -*-
@Author : Cui Jinghao
@Time : 2024/8/13 16:39
@Function: setup.py
@Contact: cuijinghao@tgqs.net
"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tgqSim',
    version='1.0.9',
    description='TGQ量子模拟器',  # 包描述
    long_description="Python for quantum simulation http://www.tiangongqs.com",  # 详细描述
    long_description_content_type='text/markdown',
    author='tiangongqs',  # 作者姓名
    license='MIT',  # 许可证
    include_package_data=True,
    packages=find_packages(include=["tgqSim", "tgqSim.*"]),
    install_requires=[
        'numpy>=1.19.0',
        'numba>=0.53.0',
        'matplotlib>=3.3.0',
        'GPUtil>=1.4.0',
        'psutil>=5.9.1',
        'pygments'
    ],
    classifiers=[
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    ],
    keywords=["tgq", "quantum", "simulator", "noise"],
)
