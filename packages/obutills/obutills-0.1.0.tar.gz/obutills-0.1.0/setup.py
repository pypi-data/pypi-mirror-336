from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="obutills",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.1",  # For YAML config support
    ],
    author="Zachary Jones",
    author_email="zacharyj@orbical.dev",
    description="A collection of utility functions and tools for Python development",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="utils, tools, system, config, logging, files",
    url="https://github.com/orbical-dev/obutills",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.6",
)
