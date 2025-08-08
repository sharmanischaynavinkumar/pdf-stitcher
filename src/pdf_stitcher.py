"""Main PDF Stitcher module."""

from typing import List
import os
import tempfile
from pypdf import PdfReader, PdfWriter
from .image_converter import ImageConverter
from .utils import validate_file_exists, get_file_extension


class PDFStitcher:
    """Main class for stitching PDFs and images together."""

    def __init__(self) -> None:
        """Initialize the PDF Stitcher."""
        self.files_to_process: List[str] = []
        self.image_converter = ImageConverter()
        self.temp_files: List[str] = []

    def add_file(self, file_path: str) -> None:
        """
        Add a file (PDF or image) to be stitched.

        Args:
            file_path: Path to the file to add

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
        """
        validate_file_exists(file_path)

        extension = get_file_extension(file_path)

        # Check if it's a PDF or supported image
        if extension == ".pdf":
            self.files_to_process.append(file_path)
        elif self.image_converter.is_image_file(file_path):
            self.files_to_process.append(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    def add_pdf(self, pdf_path: str) -> None:
        """
        Add a PDF file to be stitched.

        Args:
            pdf_path: Path to the PDF file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file is not a PDF
        """
        validate_file_exists(pdf_path)

        if get_file_extension(pdf_path) != ".pdf":
            raise ValueError(f"File is not a PDF: {pdf_path}")

        self.files_to_process.append(pdf_path)

    def add_image(self, image_path: str) -> None:
        """
        Add an image file to be stitched.

        Args:
            image_path: Path to the image file

        Raises:
            FileNotFoundError: If the file doesn't exist
            ValueError: If the file format is not supported
        """
        validate_file_exists(image_path)

        if not self.image_converter.is_image_file(image_path):
            raise ValueError(f"Unsupported image format: {image_path}")

        self.files_to_process.append(image_path)

    def add_files(self, file_paths: List[str]) -> None:
        """
        Add multiple files to be stitched.

        Args:
            file_paths: List of file paths to add
        """
        for file_path in file_paths:
            self.add_file(file_path)

    def clear_files(self) -> None:
        """Clear all files from the processing list."""
        self.files_to_process.clear()
        self._cleanup_temp_files()

    def _convert_image_to_pdf(self, image_path: str) -> str:
        """
        Convert an image to PDF and track the temporary file.

        Args:
            image_path: Path to the image file

        Returns:
            Path to the temporary PDF file
        """
        # Create temporary PDF file
        temp_fd, temp_pdf_path = tempfile.mkstemp(suffix=".pdf")
        os.close(temp_fd)

        # Convert image to PDF
        self.image_converter.convert_image_to_pdf(image_path, temp_pdf_path)

        # Track temporary file for cleanup
        self.temp_files.append(temp_pdf_path)

        return temp_pdf_path

    def _cleanup_temp_files(self) -> None:
        """Clean up temporary files."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
            except OSError:
                pass  # Ignore errors during cleanup
        self.temp_files.clear()

    def stitch(self, output_path: str) -> str:
        """
        Stitch all added files into a single PDF.

        Args:
            output_path: Path for the output PDF file

        Returns:
            Path to the created PDF file

        Raises:
            ValueError: If no files have been added
        """
        if not self.files_to_process:
            raise ValueError(
                "No files to stitch. Add files first using add_file(), add_pdf(), or add_image()."
            )

        writer = PdfWriter()

        try:
            for file_path in self.files_to_process:
                if get_file_extension(file_path) == ".pdf":
                    # Handle PDF files
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        writer.add_page(page)
                else:
                    # Handle image files - convert to PDF first
                    temp_pdf_path = self._convert_image_to_pdf(file_path)
                    reader = PdfReader(temp_pdf_path)
                    for page in reader.pages:
                        writer.add_page(page)

            # Write the combined PDF
            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            return output_path

        finally:
            # Clean up temporary files
            self._cleanup_temp_files()

    def save(self, output_path: str) -> str:
        """
        Save the stitched PDF (alias for stitch method).

        Args:
            output_path: Path for the output PDF file

        Returns:
            Path to the created PDF file
        """
        return self.stitch(output_path)

    def get_file_count(self) -> int:
        """
        Get the number of files added for stitching.

        Returns:
            Number of files in the processing list
        """
        return len(self.files_to_process)

    def get_file_list(self) -> List[str]:
        """
        Get the list of files to be stitched.

        Returns:
            Copy of the files list
        """
        return self.files_to_process.copy()

    def __enter__(self) -> "PDFStitcher":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Context manager exit - cleanup temporary files."""
        self._cleanup_temp_files()


def stitch_files(input_files: List[str], output_path: str) -> str:
    """
    Convenience function to stitch files in one call.

    Args:
        input_files: List of input file paths (PDFs and/or images)
        output_path: Path for the output PDF file

    Returns:
        Path to the created PDF file
    """
    with PDFStitcher() as stitcher:
        stitcher.add_files(input_files)
        return stitcher.stitch(output_path)
