"""Tests for Image Converter functionality."""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from src.image_converter import ImageConverter


class TestImageConverter(unittest.TestCase):
    """Test cases for ImageConverter class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.converter = ImageConverter()
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self) -> None:
        """Test ImageConverter initialization."""
        self.assertIsNotNone(self.converter.page_size)
        self.assertIsNotNone(self.converter.supported_formats)
        self.assertIn(".jpg", self.converter.supported_formats)
        self.assertIn(".png", self.converter.supported_formats)

    def test_is_image_file_valid_extensions(self) -> None:
        """Test image file detection with valid extensions."""
        valid_files = [
            "test.jpg",
            "test.jpeg",
            "test.png",
            "test.gif",
            "test.bmp",
            "test.tiff",
            "test.tif",
        ]

        for filename in valid_files:
            with self.subTest(filename=filename):
                self.assertTrue(self.converter.is_image_file(filename))

    def test_is_image_file_invalid_extensions(self) -> None:
        """Test image file detection with invalid extensions."""
        invalid_files = ["test.pdf", "test.txt", "test.doc", "test.mp4"]

        for filename in invalid_files:
            with self.subTest(filename=filename):
                self.assertFalse(self.converter.is_image_file(filename))

    def test_is_image_file_case_insensitive(self) -> None:
        """Test image file detection is case insensitive."""
        test_files = ["test.JPG", "test.JPEG", "test.PNG", "test.GIF"]

        for filename in test_files:
            with self.subTest(filename=filename):
                self.assertTrue(self.converter.is_image_file(filename))

    def test_convert_image_to_pdf_nonexistent_file(self) -> None:
        """Test converting a non-existent image file."""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_image_to_pdf("nonexistent.jpg")

    def test_convert_image_to_pdf_unsupported_format(self) -> None:
        """Test converting an unsupported file format."""
        # Create a dummy file with unsupported extension
        dummy_file = os.path.join(self.temp_dir, "test.txt")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("dummy content")

        with self.assertRaises(ValueError):
            self.converter.convert_image_to_pdf(dummy_file)

    @patch("src.image_converter.Image")
    @patch("src.image_converter.canvas")
    def test_convert_image_to_pdf_success(
        self, mock_canvas: MagicMock, mock_image: MagicMock
    ) -> None:
        """Test successful image to PDF conversion."""
        # Create a dummy image file
        test_image = os.path.join(self.temp_dir, "test.jpg")
        with open(test_image, "w", encoding="utf-8") as f:
            f.write("dummy image content")

        # Mock the Image.open context manager
        mock_img = MagicMock()
        mock_img.mode = "RGB"
        mock_img.size = (800, 600)
        mock_img.convert.return_value = mock_img
        mock_image.open.return_value.__enter__.return_value = mock_img

        # Mock the canvas
        mock_canvas_instance = MagicMock()
        mock_canvas.Canvas.return_value = mock_canvas_instance

        # Test the conversion
        output_path = self.converter.convert_image_to_pdf(test_image)

        # Verify the conversion was attempted
        mock_image.open.assert_called_once_with(test_image)
        mock_canvas.Canvas.assert_called_once()
        mock_canvas_instance.drawImage.assert_called_once()
        mock_canvas_instance.save.assert_called_once()

        # Check output path
        self.assertTrue(output_path.endswith(".pdf"))

    def test_convert_images_to_pdf_empty_list(self) -> None:
        """Test converting empty list of images."""
        with self.assertRaises(ValueError):
            self.converter.convert_images_to_pdf([], "output.pdf")

    def test_convert_images_to_pdf_nonexistent_file(self) -> None:
        """Test converting list with non-existent image."""
        with self.assertRaises(FileNotFoundError):
            self.converter.convert_images_to_pdf(["nonexistent.jpg"], "output.pdf")

    def test_convert_images_to_pdf_unsupported_format(self) -> None:
        """Test converting list with unsupported file format."""
        # Create a dummy file with unsupported extension
        dummy_file = os.path.join(self.temp_dir, "test.txt")
        with open(dummy_file, "w", encoding="utf-8") as f:
            f.write("dummy content")

        with self.assertRaises(ValueError):
            self.converter.convert_images_to_pdf([dummy_file], "output.pdf")

    @patch("src.image_converter.Image")
    @patch("src.image_converter.canvas")
    def test_convert_images_to_pdf_success(
        self, mock_canvas: MagicMock, mock_image: MagicMock
    ) -> None:
        """Test successful conversion of multiple images to PDF."""
        # Create dummy image files
        test_images = []
        for i in range(3):
            test_image = os.path.join(self.temp_dir, f"test{i}.jpg")
            with open(test_image, "w", encoding="utf-8") as f:
                f.write(f"dummy image content {i}")
            test_images.append(test_image)

        # Mock the Image.open context manager
        mock_img = MagicMock()
        mock_img.mode = "RGB"
        mock_img.size = (800, 600)
        mock_img.convert.return_value = mock_img
        mock_image.open.return_value.__enter__.return_value = mock_img

        # Mock the canvas
        mock_canvas_instance = MagicMock()
        mock_canvas.Canvas.return_value = mock_canvas_instance

        # Test the conversion
        output_path = os.path.join(self.temp_dir, "output.pdf")
        result = self.converter.convert_images_to_pdf(test_images, output_path)

        # Verify the conversion was attempted
        self.assertEqual(mock_image.open.call_count, 3)
        mock_canvas.Canvas.assert_called_once()
        self.assertEqual(mock_canvas_instance.drawImage.call_count, 3)
        self.assertEqual(mock_canvas_instance.showPage.call_count, 3)
        mock_canvas_instance.save.assert_called_once()

        # Check output path
        self.assertEqual(result, output_path)


if __name__ == "__main__":
    unittest.main()
