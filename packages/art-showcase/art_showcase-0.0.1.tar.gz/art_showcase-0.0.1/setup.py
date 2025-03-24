 

import setuptools
from setuptools import setup, find_packages

long_description = ""
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="art_showcase",
    version="0.0.1",
    author="Victor Kipkemboi",
    author_email="scriptilapia@gmail.com",
    long_description =long_description,
    long_description_content_type="text/markdown",
    description="""A simple library for custom showcasing fonts from the 'art' PyPi package , it is helpful when trying to choose a font """,
    url="https://github.com/victhepythonista/art-showcase",
    project_urls={
        "Bug Tracker": "https://github.com/victhepythonista/art-showcase/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    packages=["art_showcase"],
    python_requires=">=3.6",
 
)