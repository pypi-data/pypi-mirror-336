from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="refactoring_assistant",
    version="0.1.0",
    author="Ruslan",
    author_email="Waiper@gmail.com",
    description="Библиотека для выявления участков кода, требующих рефакторинга",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/refactoring-assistant",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)