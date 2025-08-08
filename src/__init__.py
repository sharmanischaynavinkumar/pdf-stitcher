"""PDF Stitcher package initialization."""

__version__ = "1.0.0"
__author__ = "PDF Stitcher Team"

from .pdf_stitcher import PDFStitcher
from .image_converter import ImageConverter

__all__ = ["PDFStitcher", "ImageConverter"]
