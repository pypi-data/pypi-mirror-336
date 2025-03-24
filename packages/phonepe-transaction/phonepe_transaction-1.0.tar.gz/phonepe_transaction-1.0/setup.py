from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="phonepe_transaction",
    version="1.1",
    author="Dev Pancholi",
    author_email="devpancholigt2004@gmail.com",
    description="A simplified way to integrate payments into websites and applications using API responses.",
    License="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Devpancholi04/phonepe_transaction",
    packages=find_packages(),
    install_requires = [
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6",
)