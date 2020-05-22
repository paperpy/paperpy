#!/usr/bin/env python3
import os, sys
import setuptools

# Get text from README.txt
with open("README.md", "r") as fp:
    readme_text = fp.read()

# Get __version__ without importing
with open("paperpy/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__ = "):
            exec(line)
            break

setuptools.setup(
    name="paperpy",
    version=__version__,
    description="Tools for simplifying the preparation of version-controlled and well-written academic papers.",
    license="MIT",
    keywords="paper academia academic writing write",
    author="Robin De Schepper",
    author_email="robingilbert.deschepper@unipv.it",
    url="https://github.com/paperpy/paperpy",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    packages=["paperpy"],
    include_package_data=True,
    package_data={"paperpy": ["data/**/*"]},
    entry_points={"console_scripts": ["paperpy = paperpy.cli:handle_command"],},
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=["setuptools", "pypandoc", "tabulate", "textblob"],
    extras_require={"dev": ["sphinx", "sphinx_rtd_theme>=0.4.3", "pre-commit", "black"],},
)
