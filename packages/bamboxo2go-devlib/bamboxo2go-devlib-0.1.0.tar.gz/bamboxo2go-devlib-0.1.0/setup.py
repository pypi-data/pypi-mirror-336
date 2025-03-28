from setuptools import setup, find_packages

setup(
    name="bamboxo2go-devlib",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    test_suite="tests",
    include_package_data=True,
    description="Useful library for developers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Qiang Zhou",
    author_email="qiang@bamboox2go.com",
    url="https://github.com/bamboox2go/devlib",
)
