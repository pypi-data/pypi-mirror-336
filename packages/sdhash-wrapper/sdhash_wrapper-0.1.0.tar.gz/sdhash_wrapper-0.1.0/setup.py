from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import urllib.request

class CustomInstall(install):
    """Custom installation to download and set up SDhash binary."""
    def run(self):
        sdhash_url = "https://github.com/Botacin-s-Lab/SDHash/releases/download/1.0.0/SDhash"
        binary_path = os.path.join(os.path.dirname(__file__), "sdhash_wrapper", "sdhash")

        if not os.path.exists(binary_path):
            print("Downloading SDhash binary...")
            urllib.request.urlretrieve(sdhash_url, binary_path)
            os.chmod(binary_path, 0o755)

        install.run(self)

setup(
    name="sdhash_wrapper",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],  
    include_package_data=True,
    cmdclass={"install": CustomInstall},  
    entry_points={
        "console_scripts": [
            "sdhash-python=sdhash_wrapper.wrapper:SDHash"
        ],
    },
    author="Your Name",
    author_email="mabonmn2002@gmail.com",
    description="A Python wrapper for SDHash binary.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Botacin-s-Lab/SDhash_Python",  # Update with actual GitHub repo
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
