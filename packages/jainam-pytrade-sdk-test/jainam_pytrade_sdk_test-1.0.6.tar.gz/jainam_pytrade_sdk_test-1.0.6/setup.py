import setuptools
import os
import io
from setuptools import setup
from config.config import *


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name=Props.pip_name,
    version=Props.pip_version,
    author=Props.setup_author,
    author_email=Props.setup_author_email,
    description=Props.setup_description,
    license=Props.setup_license,
    long_description="readme",
    long_description_content_type="text/markdown",
    include_package_data=True,
    url=Props.setup_url,
    download_url=Props.setup_downloadable_url,
    packages=setuptools.find_packages(),
    install_requires=["requests","pandas","websocket-client","rel"],
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Intended Audience :: Developers",
    ],

    python_requires='>=3.7',

    project_urls={
        "Documentation": Props.setup_apidocs,
    },
)