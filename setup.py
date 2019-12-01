# coding:utf8
from setuptools import setup, find_packages

with open("Readme.md", "r") as fh:
    long_description = fh.read()

setup(
    name='TetrisBattle',             
    version='1.0',           
    packages=['TetrisBattle'], 
    long_description=long_description,
    # package_data={'assets': ['assets/*']},
    # include_package_data=True,
    # exclude_package_date={'': ['.gitignore']},
    python_requires=">=3.6",
    install_requires=[         
        'pygame>=1.9.4'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
)