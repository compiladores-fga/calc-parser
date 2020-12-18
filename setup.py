import setuptools

setuptools.setup(
    name="calc-parser-renan",
    version="0.0.1",
    author="Renan Welz Schadt",
    author_email="renanschadt@gmail.com",
    description="Calculator using Lark",
    url="https://github.com/renan601/calc-parser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
