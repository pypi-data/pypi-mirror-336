# Jupyter ClipMagic

A simple IPython/Jupyter magic extension that copies code to the clipboard.

## Installation

```bash
pip install jupyter_clipmagic
```

Or using `uv`:

```bash
uv pip install jupyter_clipmagic
```

## Usage

Load the extension in your notebook:

```python
%load_ext jupyter_clipmagic
```

Copy a line to the clipboard:

```python
%clip print("Hello, world!")
```

Copy a cell to the clipboard:

```python
%%clip
for i in range(10):
    print(i)
```

## Development

Set up development environment using `uv`:

```bash
uv venv
uv pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```