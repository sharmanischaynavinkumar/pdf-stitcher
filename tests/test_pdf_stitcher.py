"""Tests for PDF Stitcher functionality."""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from src.pdf_stitcher import PDFStitcher, stitch_files


class TestPDFStitcher(unittest.TestCase):
    """Test cases for PDFStitcher class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.stitcher = PDFStitcher()
        self.temp_dir = tempfile.mkdtemp()

        # Create dummy test files
        self.test_pdf1 = os.path.join(self.temp_dir, "test1.pdf")
        self.test_pdf2 = os.path.join(self.temp_dir, "test2.pdf")
        self.test_image = os.path.join(self.temp_dir, "test.jpg")
        self.output_pdf = os.path.join(self.temp_dir, "output.pdf")

        # Create dummy files
        with open(self.test_pdf1, "w", encoding="utf-8") as f:
            f.write("dummy pdf content")
        with open(self.test_pdf2, "w", encoding="utf-8") as f:
            f.write("dummy pdf content")
        with open(self.test_image, "w", encoding="utf-8") as f:
            f.write("dummy image content")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self) -> None:
        """Test PDFStitcher initialization."""
        self.assertEqual(len(self.stitcher.files_to_process), 0)
        self.assertIsNotNone(self.stitcher.image_converter)
        self.assertEqual(len(self.stitcher.temp_files), 0)

    def test_add_pdf_valid_file(self) -> None:
        """Test adding a valid PDF file."""
        # Note: This test uses dummy files, not real PDFs
        # In a real scenario, you'd want to use actual PDF files
        self.stitcher.add_pdf(self.test_pdf1)
        self.assertEqual(len(self.stitcher.files_to_process), 1)
        self.assertIn(self.test_pdf1, self.stitcher.files_to_process)

    def test_add_pdf_nonexistent_file(self) -> None:
        """Test adding a non-existent PDF file."""
        with self.assertRaises(FileNotFoundError):
            self.stitcher.add_pdf("nonexistent.pdf")

    def test_add_pdf_wrong_extension(self) -> None:
        """Test adding a file with wrong extension as PDF."""
        with self.assertRaises(ValueError):
            self.stitcher.add_pdf(self.test_image)

    def test_add_image_valid_file(self) -> None:
        """Test adding a valid image file."""
        self.stitcher.add_image(self.test_image)
        self.assertEqual(len(self.stitcher.files_to_process), 1)
        self.assertIn(self.test_image, self.stitcher.files_to_process)

    def test_add_image_invalid_extension(self) -> None:
        """Test adding a file with invalid image extension."""
        with self.assertRaises(ValueError):
            self.stitcher.add_image(self.test_pdf1)

    def test_add_files_multiple(self) -> None:
        """Test adding multiple files at once."""
        files = [self.test_pdf1, self.test_pdf2, self.test_image]
        self.stitcher.add_files(files)
        self.assertEqual(len(self.stitcher.files_to_process), 3)

    def test_clear_files(self) -> None:
        """Test clearing files from the processing list."""
        self.stitcher.add_pdf(self.test_pdf1)
        self.stitcher.add_image(self.test_image)
        self.assertEqual(len(self.stitcher.files_to_process), 2)

        self.stitcher.clear_files()
        self.assertEqual(len(self.stitcher.files_to_process), 0)

    def test_get_file_count(self) -> None:
        """Test getting the file count."""
        self.assertEqual(self.stitcher.get_file_count(), 0)

        self.stitcher.add_pdf(self.test_pdf1)
        self.assertEqual(self.stitcher.get_file_count(), 1)

        self.stitcher.add_image(self.test_image)
        self.assertEqual(self.stitcher.get_file_count(), 2)

    def test_get_file_list(self) -> None:
        """Test getting the file list."""
        files = [self.test_pdf1, self.test_image]
        self.stitcher.add_files(files)

        file_list = self.stitcher.get_file_list()
        self.assertEqual(len(file_list), 2)
        self.assertIn(self.test_pdf1, file_list)
        self.assertIn(self.test_image, file_list)

    def test_stitch_no_files(self) -> None:
        """Test stitching with no files added."""
        with self.assertRaises(ValueError):
            self.stitcher.stitch(self.output_pdf)

    def test_context_manager(self) -> None:
        """Test using PDFStitcher as a context manager."""
        with PDFStitcher() as stitcher:
            stitcher.add_pdf(self.test_pdf1)
            self.assertEqual(stitcher.get_file_count(), 1)
        # Context manager should clean up automatically


class TestStitchFilesFunction(unittest.TestCase):
    """Test cases for the stitch_files convenience function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

        # Create dummy test files
        self.test_pdf1 = os.path.join(self.temp_dir, "test1.pdf")
        self.test_pdf2 = os.path.join(self.temp_dir, "test2.pdf")
        self.output_pdf = os.path.join(self.temp_dir, "output.pdf")

        # Create dummy files
        with open(self.test_pdf1, "w", encoding="utf-8") as f:
            f.write("dummy pdf content")
        with open(self.test_pdf2, "w", encoding="utf-8") as f:
            f.write("dummy pdf content")

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch("src.pdf_stitcher.PDFStitcher")
    def test_stitch_files_function(self, mock_stitcher_class: MagicMock) -> None:
        """Test the stitch_files convenience function."""
        # Mock the stitcher instance
        mock_stitcher = MagicMock()
        mock_stitcher_class.return_value.__enter__.return_value = mock_stitcher
        mock_stitcher.stitch.return_value = self.output_pdf

        # Test the function
        input_files = [self.test_pdf1, self.test_pdf2]
        result = stitch_files(input_files, self.output_pdf)

        # Verify calls
        mock_stitcher.add_files.assert_called_once_with(input_files)
        mock_stitcher.stitch.assert_called_once_with(self.output_pdf)
        self.assertEqual(result, self.output_pdf)


if __name__ == "__main__":
    unittest.main()
