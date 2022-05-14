# svg2json

Collects a set of svg vector graphics into a single json file using data URIs

**This project is currently in alpha stage**

## Dependencies

- scour: https://github.com/scour-project/scour

## Build

```bash
./pkg-build
```

## Install

```bash
cd dist
sudo pip install --upgrade svg2json-0.1.0-py3-none-any.whl
```

## Usage

```bash
svg2json --help
```

```bash
svg2json -o iconset.json iconset/*.svg
```

```bash
svg2json good.svg bad.svg > status.json
```

Example of a generated JSON file:
```json
{
    "SVG a": "data:image/svg+xml;base64,<data>",
    "SVG b": "data:image/svg+xml;base64,<data>"
}
```

