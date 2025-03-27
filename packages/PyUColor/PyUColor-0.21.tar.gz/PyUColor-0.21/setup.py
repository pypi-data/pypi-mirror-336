from setuptools import setup, find_packages

# Read the content of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="PyUColor",
    version='0.21',
    packages=find_packages(),
    install_requires=[
        
    ],
    description="A simple library for printing colored text in the terminal.",
)