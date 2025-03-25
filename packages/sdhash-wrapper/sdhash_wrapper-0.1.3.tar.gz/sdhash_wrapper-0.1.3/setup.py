from setuptools import setup, find_packages
import os

setup(
    name="sdhash_wrapper",
    version="0.1.3",
    packages=find_packages(),
    include_package_data=True,
    package_data={"sdhash_wrapper": ["sdhash"]},  # Ensure binary is included
    install_requires=[],
    entry_points={
        "console_scripts": [
            "sdhash-python=sdhash_wrapper.wrapper:SDHash"
        ],
    },
    author="Mabon Ninan",
    author_email="mabonmn2002@gmail.com",
    description="A Python wrapper for SDHash binary.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Botacin-s-Lab/SDhash_Python",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
