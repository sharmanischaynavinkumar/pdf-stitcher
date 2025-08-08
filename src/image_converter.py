"""Image to PDF converter module."""

from typing import List, Optional, Tuple
import os
from pathlib import Path
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile


class ImageConverter:
    """Converts images to PDF format."""

    def __init__(self, page_size: Tuple[float, float] = A4):
        """
        Initialize the ImageConverter.

        Args:
            page_size: Page size for the PDF (default: A4)
        """
        self.page_size = page_size
        self.supported_formats = {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".bmp",
            ".tiff",
            ".tif",
        }

    def is_image_file(self, file_path: str) -> bool:
        """
        Check if the file is a supported image format.

        Args:
            file_path: Path to the file

        Returns:
            True if the file is a supported image format
        """
        return Path(file_path).suffix.lower() in self.supported_formats

    def convert_image_to_pdf(
        self, image_path: str, output_path: Optional[str] = None
    ) -> str:
        """
        Convert a single image to PDF.

        Args:
            image_path: Path to the input image
            output_path: Path for the output PDF (optional)

        Returns:
            Path to the created PDF file
        """
        if not self.is_image_file(image_path):
            raise ValueError(f"Unsupported image format: {image_path}")

        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Generate output path if not provided
        if output_path is None:
            base_name = Path(image_path).stem
            output_path = f"{base_name}.pdf"

        # Open and process the image
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode != "RGB":
                img = img.convert("RGB")

            # Calculate the size to fit the page while maintaining aspect ratio
            img_width, img_height = img.size
            page_width, page_height = self.page_size

            # Calculate scaling factor
            scale_x = page_width / img_width
            scale_y = page_height / img_height
            scale = min(scale_x, scale_y)

            # Calculate new dimensions
            new_width = img_width * scale
            new_height = img_height * scale

            # Center the image on the page
            x_offset = (page_width - new_width) / 2
            y_offset = (page_height - new_height) / 2

            # Create PDF
            c = canvas.Canvas(output_path, pagesize=self.page_size)

            # Save image to temporary file for ReportLab
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                img.save(temp_file.name, "PNG")
                temp_path = temp_file.name

            try:
                # Draw image on PDF
                c.drawImage(
                    temp_path, x_offset, y_offset, width=new_width, height=new_height
                )
                c.save()
            finally:
                # Clean up temporary file
                os.unlink(temp_path)

        return output_path

    def convert_images_to_pdf(self, image_paths: List[str], output_path: str) -> str:
        """
        Convert multiple images to a single PDF.

        Args:
            image_paths: List of paths to input images
            output_path: Path for the output PDF

        Returns:
            Path to the created PDF file
        """
        if not image_paths:
            raise ValueError("No image paths provided")

        # Validate all image files
        for image_path in image_paths:
            if not self.is_image_file(image_path):
                raise ValueError(f"Unsupported image format: {image_path}")
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

        # Create PDF with multiple pages
        c = canvas.Canvas(output_path, pagesize=self.page_size)

        for image_path in image_paths:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != "RGB":
                    img = img.convert("RGB")

                # Calculate the size to fit the page while maintaining aspect ratio
                img_width, img_height = img.size
                page_width, page_height = self.page_size

                # Calculate scaling factor
                scale_x = page_width / img_width
                scale_y = page_height / img_height
                scale = min(scale_x, scale_y)

                # Calculate new dimensions
                new_width = img_width * scale
                new_height = img_height * scale

                # Center the image on the page
                x_offset = (page_width - new_width) / 2
                y_offset = (page_height - new_height) / 2

                # Save image to temporary file for ReportLab
                with tempfile.NamedTemporaryFile(
                    suffix=".png", delete=False
                ) as temp_file:
                    img.save(temp_file.name, "PNG")
                    temp_path = temp_file.name

                try:
                    # Draw image on PDF
                    c.drawImage(
                        temp_path,
                        x_offset,
                        y_offset,
                        width=new_width,
                        height=new_height,
                    )
                    c.showPage()  # Move to next page
                finally:
                    # Clean up temporary file
                    os.unlink(temp_path)

        c.save()
        return output_path
