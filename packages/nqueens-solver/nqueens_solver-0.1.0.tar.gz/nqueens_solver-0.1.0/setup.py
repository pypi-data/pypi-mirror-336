from setuptools import setup, find_packages

setup(
    name="nqueens-solver",  # Package name (must be unique in PyPI)
    version="0.1.0",  # First release version
    author="Durkesh",
    author_email="durkeshpanuja@gmail.com",
    description="A Python library to solve the N-Queens problem efficiently.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/durkesh-datasci/n-queens-solver",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
