# LDIF to JSON Converter

[![PyPI version](https://badge.fury.io/py/ldif2json.svg)](https://pypi.org/project/ldif2json/)
[![Python versions](https://img.shields.io/pypi/pyversions/ldif2json.svg)](https://pypi.org/project/ldif2json/)

A Python tool to convert LDIF files to JSON format with optional hierarchical nesting.

## Features

- Convert LDIF to JSON format
- Handle multivalued attributes
- Optional hierarchical nesting of entries
- Support for stdin/stdout
- Configurable JSON indentation

## Installation

```bash
pip install ldif2json
```

## Usage

Basic conversion:
```bash
ldif2json input.ldif -o output.json
```

With hierarchical nesting:
```bash
ldif2json input.ldif --nest -o output.json
```

Using pipes:
```bash
ldapsearch -x -b "dc=example,dc=com" | ldif2json --nest children
```

## Options

```
usage: ldif2json [-h] [-o OUTPUT] [-i INDENT] [-n [ATTR]] [input_file]

positional arguments:
  input_file            LDIF input file (use - for stdin)

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output JSON file (default: stdout)
  -i INDENT, --indent INDENT
                        Indentation level for JSON output (default: 2)
  -n [ATTR], --nest [ATTR]
                        Enable hierarchical nesting using specified attribute (default: "subEntries" when flag used without value)
```

## License

MIT
