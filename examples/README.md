# Example Usage

This directory contains examples of how to use the PDF Stitcher.

## Sample Files

- `sample_document.md` - A sample document that can be converted to PDF
- `usage_examples.py` - Python script examples

## Basic Usage Examples

### Command Line

```bash
# Stitch PDFs only
python pdf_stitcher.py -i document1.pdf -i document2.pdf -o combined.pdf

# Mix PDFs and images
python pdf_stitcher.py -i report.pdf -i chart.png -i graph.jpg -o final_report.pdf

# Use the info command to inspect files
python pdf_stitcher.py info document.pdf image.jpg

# Stitch all files in a directory
python pdf_stitcher.py stitch-directory ./documents/ -o combined.pdf
```

### Python API

```python
from src.pdf_stitcher import PDFStitcher

# Create stitcher instance
stitcher = PDFStitcher()

# Add files
stitcher.add_pdf("document1.pdf")
stitcher.add_pdf("document2.pdf")
stitcher.add_image("chart.png")

# Save combined PDF
stitcher.save("output.pdf")
```

## Tips

1. **File Order**: Files are processed in the order they are added
2. **Image Quality**: Images are automatically scaled to fit the page while maintaining aspect ratio
3. **Large Files**: For many large files, consider processing in batches
4. **Supported Formats**: 
   - PDFs: `.pdf`
   - Images: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif`
