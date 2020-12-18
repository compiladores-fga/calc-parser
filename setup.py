from setuptools import setup, find_packages

# This call to setup() does all the work
setup(
    name="simple-calc",
    version="0.0.1",
    description="Simple calculator built in Lark",
    url="https://github.com/romulosouza/calc-parser",
    packages=find_packages(),
    author="Rômulo Souza",
    author_email="romulovinicius10@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=3.7'
)
