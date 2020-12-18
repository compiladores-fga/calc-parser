import setuptools

setuptools.setup(
    name="calc-parser",
    version="0.0.1",
    author="Sara Silva",
    author_email="saracsas2@gmail.com",
    description="A calculator with Lark",
    url="https://github.com/silvasara/calc-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
