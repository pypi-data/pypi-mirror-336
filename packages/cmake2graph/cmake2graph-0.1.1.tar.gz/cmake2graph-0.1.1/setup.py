from setuptools import setup, find_packages

setup(
    name="cmake2graph",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "networkx",
        "matplotlib",
    ],
    entry_points={
        "console_scripts": [
            "cmake2graph=cmake2graph.cli:main",
        ],
    },
    extras_require={
        "test": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
        ],
    },
    author="Kenneth Assogba",
    author_email="kennethassogba@gmail.com",
    description="Visualize CMake target dependencies as a directed graph",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/kennethassogba/cmake2graph",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
