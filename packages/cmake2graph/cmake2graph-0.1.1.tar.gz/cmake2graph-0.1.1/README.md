# cmake2graph

A tool to visualize CMake target dependencies as a directed graph.

## Installation

```bash
pip install cmake2graph
```

To install the package locally for development:

```bash
cd cmake2graph
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flake8 pytest pytest-cov
pip install -e .[test]
pytest --cov=cmake2graph # test
```

## Usage

```bash
cmake2graph /path/to/cpp-cmake-project
cmake2graph /path/to/cpp-cmake-project --exclude-external --output graph.png --target my_target --depth 2
```

Produces

![Example](example.png)

## Features

- Parse CMake files recursively
- Generate dependency graphs
- Filter by specific targets
- Control dependency depth
- Exclude external libraries (not working yet)
- Export to various image formats
