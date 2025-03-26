from setuptools import setup, find_packages

setup(
    name="ContainedSDK",
    version="0.0.0",
    packages=find_packages(),
    author="Ben Hall",
    description="",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
)

