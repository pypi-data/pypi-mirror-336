from setuptools import setup, find_packages

setup(
    name="llm-memory",
    version="0.2.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "tinydb>=4.7.0",
    ],
    author="likunpm",
    author_email="likun2440@gmail.com",  
    description="A memory management system for large language models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/likunpm/llm-memory",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)