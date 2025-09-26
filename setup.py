from setuptools import setup, find_packages

setup(
    name="tufteplotlib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.0"
    ],
    author="Jon Woolfrey",
    description="An extension to matplotlib for creating graphs in the style of Edward Tufte.",
    url="https://github.com/woolfrey/tufteplotlib",
)

