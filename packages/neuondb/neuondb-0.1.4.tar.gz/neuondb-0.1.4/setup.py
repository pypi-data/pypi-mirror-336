# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 18:52:15 2024

@author: yangl
"""

from setuptools import setup, find_packages

setup(
      name="neuondb",
      version="0.1.4",
      author="holmes",
      author_email="tidusyuna88@gmail.com",
      description="Wrapper for MongoDB using pymongo",
      packages=find_packages(),
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
      python_requires=">=3.6",
      install_requires=[
        "pymongo>=4.7.3",  
        "neuon>=0.0.1",     
      ],
      )
