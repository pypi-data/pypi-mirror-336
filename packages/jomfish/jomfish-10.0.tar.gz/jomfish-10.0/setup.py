from setuptools import setup, find_packages
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jomfish",
    version="10.0",
    author="Jimmy Luong",
    author_email="nguyenhungjimmy.luong@gmail.com",
    description="Jomfish - A high-performance chess engine",
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    packages=find_packages(),  
    package_data={"jomfish": ["bin/jomfish.exe"]},  
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "jomfish = jomfish.wrapper:main",  
        ],
    },
    classifiers=[
        "Programming Language :: Rust",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)
