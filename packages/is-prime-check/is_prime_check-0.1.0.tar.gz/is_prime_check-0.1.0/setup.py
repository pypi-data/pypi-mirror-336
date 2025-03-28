from setuptools import setup, find_packages

setup(
    name="is_prime_check",
    version="0.1.0",
    author="Somdev Das",
    author_email="somdev4g@gmail.com",
    description="A simple package to check if a number is prime",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/imsomdev/is_prime",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
