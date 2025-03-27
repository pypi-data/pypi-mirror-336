# @Coding: UTF-8
# @Time: 2025/3/26 21:16
# @Author: xieyang_ls
# @Filename: setup.py

from setuptools import setup, find_packages

setup(
    name="pyutils_spirit",  # 包名（PyPI唯一标识）
    version="1.1.5",  # 版本号（每次上传需更新）
    author="Spirit",
    author_email="2969643689@qq.com",
    description="A Small Python package",
    packages=find_packages(include=["pyutils_spirit", "pyutils_spirit.*"]),  # 自动发现所有包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Python版本要求
    install_requires=[],  # 依赖列表（如 ["requests>=2.25.1"]）
)
