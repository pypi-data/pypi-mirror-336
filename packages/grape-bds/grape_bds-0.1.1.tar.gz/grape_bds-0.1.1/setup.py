import pathlib
from setuptools import setup, find_packages

# Read the README file for the long description
HERE = pathlib.Path(__file__).parent
long_description = (HERE / "README.md").read_text()

setup(
    name="grape_bds",
    version="0.1.1",
    author="Allan de Lima",
    description="Grammatical Evolution framework built with DEAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "deap"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)