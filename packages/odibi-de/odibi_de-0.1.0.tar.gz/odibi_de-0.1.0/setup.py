# -*- coding: utf-8 -*-
import io
from setuptools import setup, find_packages

setup(
    name="odibi_de",
    version="0.1.0",  # Update this for every new release
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "fastavro",
        "fsspec",
        "pyarrow",
        "azure-storage-blob",
        "pyspark",
        "pyodbc"
    ],
    author="Henry Odibi",
    author_email="henryodibi@outlook.com",
    description="Personal data engineering framework using Pandas and Spark",
    long_description=io.open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/henryodibi11/odibi_de_project",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
