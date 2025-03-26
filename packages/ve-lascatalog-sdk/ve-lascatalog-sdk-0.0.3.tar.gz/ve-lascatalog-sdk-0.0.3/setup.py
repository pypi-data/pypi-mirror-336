# coding:utf-8

from setuptools import setup, find_packages
from pathlib import Path

install_requires = [
    "requests>=2.25.1,<=2.28.1",
    "retry>=0.9.2,<=0.10.0",
    "six>=1.16.0,<=1.17.0"
]
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()
setup(
    name="ve-lascatalog-sdk",
    version='0.0.3',
    keywords=("las-rest", "las_catalog_sdk"),
    description="The Las Metadata SDK for Python",
    author="bytedance",
    packages=find_packages(exclude=["tests", "tests.*", "test", "test.*"]),
    python_requires='>=3.1',
    install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
