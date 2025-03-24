# JAS - Custom Text Compression Library

[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](htmlcov/index.html)

JAS Compression is a custom text compression library that uses tokenization, specialized preprocessing for different text-based formats, and deterministic Huffman encoding to compress and decompress text files. The project is designed to handle plain text, JSON, CSV, XML, and YAML formats.

## Features

- **Tokenization:** Breaks text into tokens (words, punctuation, whitespace, etc.).
- **Special Phrase Detection:** Identifies and replaces frequently occurring special phrases to improve compression.
- **Deterministic Huffman Encoding:** Uses a deterministic Huffman tree for consistent encoding and decoding.
- **Format-Specific Preprocessing:** Supports normalization for JSON, CSV, XML, and YAML files.
- **Command-Line Interface:** Provides a CLI for compression and decompression with verbose logging and progress bars.

## Installation

You can install the package via PyPI:

```bash
pip install jas-compression

```
Or, for the latest development version, clone the repository and install it locally:

```bash
git clone https://github.com/yourusername/jas-compression.git
cd jas
pip install .
```

## Usage
# Compression

To compress a text file:
```bash
python -m jas.cli compress input.txt output.jas --verbose
```

# Decompression

To decompress a .jas file:
```bash
python -m jas.cli decompress output.jas result.txt --verbose
```

## Project Structure
```bash
jas-compression/
├── jas/
│   ├── __init__.py
│   ├── compressor.py
│   ├── decompressor.py
│   ├── cli.py
│   ├── huffman.py
│   ├── tokenizer.py
│   ├── structured.py
│   ├── utils.py
│   └── bitstream.py
├── README.md
├── setup.py
├── MANIFEST.in
├── LICENSE
└── requirements.txt
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub. Make sure to follow the existing code style and include tests for any new features.

## License
This project is licensed under the MIT License.