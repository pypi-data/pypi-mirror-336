from setuptools import setup, find_packages

setup(
    name="altogether",
    version="0.1.0",
    description="Promise.all for Python: run blocking operations in parallel",
    author="Sunghyun Cho",
    author_email="hey@cho.sh",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.7",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
