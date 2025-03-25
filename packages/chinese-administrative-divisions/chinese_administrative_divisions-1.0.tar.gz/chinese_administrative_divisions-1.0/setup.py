# setup.py
from setuptools import setup, find_packages

setup(
    name="chinese_administrative_divisions",
    version="1.0",
    packages=find_packages(),
    description="中国行政区划查询包",
    long_description=open("README.md",encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="wangxueming",
    author_email="zgxdxf@hotmail.com",
    url="https://github.com/zgxdxf/good-fortune.git",
classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)