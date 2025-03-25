from setuptools import setup, find_packages

setup(
    name="mlscore",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "scikit-learn>=0.24.0",
    ],
    author="sachin kuamr",
    author_email="sachin18449kumar@gmail.com",
    description="A comprehensive machine learning evaluation metrics library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sachin62025/mlscore",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
) 