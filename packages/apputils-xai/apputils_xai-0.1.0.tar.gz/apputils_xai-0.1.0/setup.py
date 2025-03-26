from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="apputils-xai",
    version="0.1.0",
    author="NoLink Team",
    author_email="your.email@example.com",
    description="A utility library for no-code app generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sumedh1599/apputils-xai",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)