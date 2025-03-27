from setuptools import find_packages, setup

setup(
    name="cython-build-helper",
    version="0.3.0",
    description="A helper for building Cython projects with flexible file copying and module building.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="xfally",
    author_email="coolwinding@foxmail.com",
    url="https://github.com/xfally/cython-build-helper",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "Cython>=3.0.12",
    ],
)
