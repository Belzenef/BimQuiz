#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.txt", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Bimquizz",
    version="0.0.1",
    author="ejacquemet",
    author_email="elise.jacquemet@hotmail.fr",
    description="Quiz en réseau",
    long_description=long_description,
    long_description_content_type="text",
    url="https://github.com/Belzenef/Quizz",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)


