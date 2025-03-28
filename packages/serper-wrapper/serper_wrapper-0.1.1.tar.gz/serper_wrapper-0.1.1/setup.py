from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="serper-wrapper",
    version="0.1.1",
    author="Serper Wrapper",
    author_email="your.email@example.com",
    description="Python package for calling Serper API with support for disk and MongoDB caching",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/serper-wrapper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "pymongo>=3.11.0",
        "prometheus_client>=0.12.0",
    ],
    extras_require={
        "mongo": ["pymongo>=3.11.0"],
        "metrics": ["prometheus_client>=0.12.0"],
        "all": ["pymongo>=3.11.0", "prometheus_client>=0.12.0"],
    },
)