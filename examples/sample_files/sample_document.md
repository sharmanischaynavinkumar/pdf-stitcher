# Sample Document

This is a sample markdown document that can be converted to PDF and used for testing the PDF stitcher.

## Introduction

The PDF Stitcher is a powerful tool for combining multiple PDF documents and images into a single cohesive document.

## Features

### Core Functionality
- Combine multiple PDF files
- Convert images to PDF and include them
- Maintain page order and quality
- Support for various image formats

### Supported Formats

**PDF Files:**
- Standard PDF documents
- Password-protected PDFs (with proper credentials)

**Image Files:**
- JPEG (.jpg, .jpeg)
- PNG (.png) 
- GIF (.gif)
- BMP (.bmp)
- TIFF (.tiff, .tif)

## Usage Examples

### Command Line
```bash
# Basic stitching
python pdf_stitcher.py -i file1.pdf -i file2.pdf -o combined.pdf

# Mixed content
python pdf_stitcher.py -i report.pdf -i chart.png -o final.pdf
```

### Python API
```python
from src.pdf_stitcher import PDFStitcher

stitcher = PDFStitcher()
stitcher.add_pdf("document.pdf")
stitcher.add_image("image.jpg")
stitcher.save("output.pdf")
```

## Benefits

1. **Efficiency**: Combine multiple documents quickly
2. **Quality**: Maintains original document quality
3. **Flexibility**: Mix different file types
4. **Automation**: Can be integrated into workflows

## Conclusion

The PDF Stitcher provides a simple yet powerful solution for document management and combination tasks.
