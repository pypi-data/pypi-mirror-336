from setuptools import setup, find_packages
import os

# Read the contents of README.md file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

# Read requirements from requirements.txt
with open("requirements.txt", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="surfnet",
    version="0.2.0",
    description="A powerful web scraping package with integrated search, captcha handling, and hardware optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dead Depth",
    author_email="transformtrails@gmail.com",
    url="https://github.com/libdo96/surfnet",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    keywords="web scraping, search, captcha, crawler, parallel processing, gpu acceleration, high throughput",
) 