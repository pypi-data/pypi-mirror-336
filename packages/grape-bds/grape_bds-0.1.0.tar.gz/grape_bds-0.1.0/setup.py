from setuptools import setup, find_packages

setup(
    name="grape_bds",
    version="0.1.0",
    author="Allan de Lima",
    description="Grammatical Evolution framework built with DEAP",
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