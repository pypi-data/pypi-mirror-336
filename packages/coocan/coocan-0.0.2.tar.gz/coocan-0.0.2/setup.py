from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="coocan",
    version="0.0.2",
    author="wauo",
    author_email="markadc@126.com",
    description="Air Spider Framework",
    packages=find_packages(),
    python_requires=">=3.10",
    long_description=long_description,
    long_description_content_type="text/markdown",
)
