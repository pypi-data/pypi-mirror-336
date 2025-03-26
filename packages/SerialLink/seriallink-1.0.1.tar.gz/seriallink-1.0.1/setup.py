from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
long_description = ""
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="SerialLink",
    packages=["seriallink"],
    version="1.0.1",
    license="MIT",
    description="SerialLink is a Python library designed to simplify serial communication with microcontrollers",
    long_description=long_description,
    url="https://github.com/Michael-Jalloh/SerialLink",
    long_description_content_type= "text/markdown",
    author="Michael Jalloh",
    author_email="michaeljalloh19@gmail.com",
    install_requires=["pyserial"],
    package_dir={"seriallink":"src/seriallink"},
    classifiers= [
        "Development Status :: 4 - Beta",      
        "Intended Audience :: Developers",      
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    platforms=["any"],
    keywords=["seriallink","serial","link","communication","microcontroller"],
    project_urls={
        "issues": "https://github.com/Michael-Jalloh/SerialLink/issues",
        "source": "https://github.com/Michael-Jalloh/SerialLink"
    },
)