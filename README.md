# PDF Stitcher

A Python application to combine multiple PDFs and images into a single PDF document.

## Features

- Stitch multiple PDF files together
- Convert images to PDF and combine with existing PDFs
- Support for various image formats (PNG, JPEG, GIF, BMP, TIFF)
- Command-line interface for easy usage
- Configurable page ordering and orientation
- Quality control for image conversion

## Requirements

- Python 3.8+
- PyPDF2 or pypdf for PDF manipulation
- Pillow (PIL) for image processing
- ReportLab for PDF creation

## Installation

### Using DevContainer (Recommended)

This project includes a devcontainer configuration for VS Code. Simply:

1. Open the project in VS Code
2. Install the "Dev Containers" extension
3. Press `Ctrl+Shift+P` and select "Dev Containers: Reopen in Container"

### Manual Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

```bash
# Stitch multiple PDFs
python pdf_stitcher.py --input file1.pdf file2.pdf file3.pdf --output combined.pdf

# Combine PDFs and images
python pdf_stitcher.py --input document.pdf image1.jpg image2.png --output result.pdf

# Specify page order and orientation
python pdf_stitcher.py --input *.pdf --output combined.pdf --orientation portrait
```

### Python API

```python
from pdf_stitcher import PDFStitcher

stitcher = PDFStitcher()

# Add files to stitch
stitcher.add_pdf("document1.pdf")
stitcher.add_pdf("document2.pdf")
stitcher.add_image("image.jpg")

# Save the combined PDF
stitcher.save("output.pdf")
```

## Project Structure

```
pdf-stitcher/
├── .devcontainer/
│   ├── devcontainer.json
│   └── Dockerfile
├── src/
│   ├── __init__.py
│   ├── pdf_stitcher.py
│   ├── image_converter.py
│   └── utils.py
├── tests/
│   ├── __init__.py
│   ├── test_pdf_stitcher.py
│   └── test_image_converter.py
├── examples/
│   └── sample_files/
├── requirements.txt
├── requirements-dev.txt
├── setup.py
└── README.md
```

## Development

The project uses a devcontainer for consistent development environment. All dependencies are automatically installed when you open the project in the devcontainer.

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/ tests/
```

## License

MIT License
