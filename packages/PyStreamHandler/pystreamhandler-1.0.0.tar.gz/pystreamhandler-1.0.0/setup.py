from setuptools import setup, find_packages

setup(
    name="pystreamhandler",
    version="1.0.0",
    description="PyStreamHandler is a lightweight Python package designed to facilitate reading and writing binary data from buffers using Python's built-in `struct` module and `bytearray`.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Christoffer Hansen",
    author_email="chris.hansen.ch@outlook.com",
    url="https://www.github.com/hansenchristoffer/pystreamhandler",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
