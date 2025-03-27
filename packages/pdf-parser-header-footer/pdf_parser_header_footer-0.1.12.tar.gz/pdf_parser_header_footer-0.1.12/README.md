# PDF Parser with Header and Footer

A Python package for automatically detecting and extracting headers, body text, and footers from PDF documents. The package supports multiple languages and provides both visual boundary detection and structured text extraction with advanced processing capabilities including markdown conversion and grammar correction for Spanish language.


## Features

- 📄 Automatic detection of headers, footers, and body sections in PDF documents
- 🌍 Multi-language support 
- 🎯 Precise boundary detection for consistent text extraction
- 📊 JSON output with structured content
- 👁️ Visual PDF output showing detected boundaries
- 📁 Process single files or entire directories
- ⚙️ Flexible configuration options
- 📝 Markdown conversion with intelligent formatting
- ✍️ Grammar correction for extracted text in Spanish
- 📚 ML-based title and text structure detection
- 🔄 Smart line joining for improved readability

## Installation

```bash
pip install pdf-parser-header-footer
```

## Quick Start

```python
from pdf_parser_header_footer import PDFSectionParser, ParserConfig
from pathlib import Path
# Use default settings (generate both PDF and JSON)
parser = PDFSectionParser()
parser.parse("path/to/document.pdf")

# Custom configuration
config = ParserConfig(
    generate_boundaries_pdf=True,
    generate_json=True,
    parse_to_markdown=True,  # Enable markdown conversion
    grammar_correction=True,  # Enable grammar correction for Spanish text
    output_dir=Path("custom/output/dir")
)
parser = PDFSectionParser(config)
parser.parse("path/to/pdf/directory")
```

## Configuration Options


| Parameter | Default | Description |
|-----------|---------|-------------|
| `generate_boundaries_pdf` | True | Generate PDF with visual boundary markers |
| `generate_json` | True | Generate JSON output with structured content |
| `parse_to_markdown` | True | Convert extracted text to markdown format |
| `grammar_correction` | True | Apply grammar correction to the extracted text in Spanish |
| `output_dir` | None | Custom output directory (default: same as input) |


## Output Format

### JSON Output
```json
{
    "pdf_with_lines": "document_final_boundaries.pdf",
    "pages": [
        {
            "number": 1,
            "header": "Header text...",
            "body": "Main content...",
            "footer": "Footer text..."
        }
    ]
}
```

### Visual PDF Output
The package generates a PDF file with colored lines showing detected boundaries:
- 🔵 Blue lines: Header boundaries
- 🟢 Green lines: Bottom footer boundaries
- 🔴 Red lines: Right footer boundaries

## Advanced Features

### Markdown Conversion
The `parse_to_markdown` option enables intelligent conversion of PDF text to markdown format:

- Automatic detection and formatting of titles and headings
- Proper handling of bullet points and numbered lists
- Table structure preservation
- Smart line joining for paragraphs
- Figure and image reference formatting

### Grammar Correction
The `grammar_correction` option applies language-specific grammar and spelling corrections for Spanish language:

- Fixes hyphenated words that were split across lines
- Corrects common OCR errors
- Uses Hunspell dictionaries for spell checking
- Caches corrections for efficiency

### Machine Learning Components

The package uses ML classifiers to improve text processing:

- **Title Classifier**: Detects and properly formats section titles and headings
- **Line Joiner Classifier**: Intelligently determines when lines should be joined into paragraphs


## Requirements

- Python 3.8 or higher
- PyMuPDF (1.24.0 or higher)
- PyMuPDF4LLM (0.0.17 or higher)
- spylls.hunspell
- spaCy with Spanish language model
- scikit-learn
- tqdm

## Examples

### Process Single File with Basic Settings
```python
from pdf_parser_header_footer import PDFSectionParser

parser = PDFSectionParser()
parser.parse("document.pdf")
```

### Process Directory with Advanced Features
```python
from pdf_parser_header_footer import PDFSectionParser, ParserConfig
from pathlib import Path

config = ParserConfig(
    generate_boundaries_pdf=True,
    generate_json=True,            
    parse_to_markdown=True,        # Enable conversion to markdown
    grammar_correction=True,       # Enable grammar correction
    output_dir=Path("output_dir")  # Custom output directory
)

parser = PDFSectionParser(config)
parser.parse("path/to/pdf/directory")
```

### Disable Specific Features
```python
from pdf_parser_header_footer import PDFSectionParser, ParserConfig

config = ParserConfig(
    generate_boundaries_pdf=False,  # Skip boundary PDF generation
    generate_json=True,             # Generate JSON output
    parse_to_markdown=True,         # Enable markdown conversion
    grammar_correction=False        # Disable grammar correction
)

parser = PDFSectionParser(config)
parser.parse("document.pdf")
```

## Processing Pipeline

The package follows this processing sequence:

1. Detect header and footer boundaries in the PDF
2. Split the document into header, body, and footer sections
3. Generate visualizations of detected boundaries
4. Extract text from each section
5. Convert extracted text to markdown (if enabled)
6. Apply grammar correction only for Spanish texts (if enabled)
7. Generate structured JSON output

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU Affero General Public License v3 (AGPL-3.0).

This program incorporates work covered by the following copyright and permission notices:

PyMuPDF (https://github.com/pymupdf/PyMuPDF)
Copyright (c) 2016-2024 Artifex Software, Inc.
Licensed under GNU Affero General Public License version 3

## Contact

Tamara Orlich - [tamara.orlich@borah.agency]

Project Link: [https://github.com/BorahLabs/pdf_parser_with_header_footer/]
