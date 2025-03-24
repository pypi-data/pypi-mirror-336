# setup.py
from setuptools import setup, find_packages

setup(
    name="printpkg",  # Replace with your package name
    version="0.2",
    packages=find_packages(),
    description="A simple package to print predefined texts",
    author="Your Name",
    author_email="your.email@example.com",
    install_requires=["pyperclip>=1.8.0"]
)
