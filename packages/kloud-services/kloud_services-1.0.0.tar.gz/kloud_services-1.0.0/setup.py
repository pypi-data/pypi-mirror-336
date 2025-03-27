from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kloud-services",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3",
        "pydantic>=2.0.0"
    ],
    description="This package provides convenient access to the GenAI Models' REST API from any Python 3.7+ application.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Raj Aryan",
    author_email="raj@kloudstac.com",
    url="https://github.com/mr-rsr/ks_opeanai",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)