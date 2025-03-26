'''
Author: zengkeyao
Date: 2025-03-13 12:57:08
LastEditors: zengkeyao
LastEditTime: 2025-03-13 14:49:36
Description: description
'''
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='ToolsFor302',
    version='0.3.0',
    description="some tools for 302",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="",
    author="zengkeyao",
    author_email='cengkeyao186@Gmail.com',
    # packages=find_packages(),
    packages=['ToolsFor302',],
    license='MIT License',
    python_requires='>=3',
)