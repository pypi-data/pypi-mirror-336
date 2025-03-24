# Aethermark

Aethermark is a C++ extension for Python built using Pybind11 and CMake. This project demonstrates how to integrate C++ code with Python and automate versioning, building, and publishing.

## Installation

You can install Aethermark from PyPI once published:

```sh
pip install aethermark
```

Alternatively, to install from source:

```sh
git clone https://github.com/yourusername/aethermark.git
cd aethermark
pip install .
```

## Usage

Once installed, you can use Aethermark in Python as follows:

```python
import aethermark
print(aethermark.add(2, 3))  # Outputs: 5
print(aethermark.subtract(5, 2))  # Outputs: 3
```

## Building from Source

### Requirements

- Python 3.7+
- CMake 3.4+
- A C++ compiler (GCC, Clang, or MSVC)
- `pip install scikit-build`

### Steps

To build the package locally:

```sh
git clone https://github.com/yourusername/aethermark.git
cd aethermark
pip install .
```

Or, to build manually:

```sh
mkdir build
cd build
cmake ..
make -j
```

## Publishing to PyPI

### 1. Update Version

Ensure the `VERSION` file in the root contains the correct version (e.g., `0.1.0`).

### 2. Build the Distribution

```sh
pip install build twine
python -m build
```

### 3. Upload to PyPI

```sh
twine upload dist/*
```

## Automating Releases with GitHub Actions

To trigger a release manually:

1. Push a new commit with an updated `VERSION` file.
2. Run the `publish.yml` GitHub Action workflow.

## Contributing

Pull requests are welcome! Please ensure your changes follow the project structure and best practices.

## License

MIT License. See `LICENSE` for details.

---

Notes
Using a virtual environment prevents conflicts with system-wide dependencies.

```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip setuptools wheel pytest
```

Always remove old build artifacts before building to prevent stale binaries from interfering.

```bash
rm -rf build dist *.egg-info
python3 setup.py clean
python3 setup.py bdist_wheel
```

Instead of running tests inside the build directory, install the generated wheel and test it as an installed package (like your users would).

```bash
pip install --force-reinstall dist/aethermark-*.whl
pytest
```
