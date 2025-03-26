from setuptools import setup, find_packages

setup(
    name="expCon",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Sandeep Jha",
    author_email="sandeepjhavc@gmail.com",
    description="A Python package for converting and evaluating infix, postfix, and prefix expressions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/expression_converter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
