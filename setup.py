#!/usr/bin/env python
from setuptools import setup
from io import open

def read(filename):
    with open(filename, encoding='utf-8') as file:
        return file.read()

setup(name='roschatBotPythonSDK',
      version='0.0.1',
      long_description=read('README.md'),
      long_description_content_type="text/markdown",
      author='tinychief',
      url='https://github.com/roschat/roschat-bot-python-sdk',
      install_requires=['requests', 'six'],
      )