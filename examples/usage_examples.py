#!/usr/bin/env python3
"""
PDF Stitcher Usage Examples

This script demonstrates various ways to use the PDF Stitcher library.
"""
import os


from src.pdf_stitcher import PDFStitcher
from src.image_converter import ImageConverter


def example_basic_stitching() -> None:
    """Example: Basic PDF stitching."""
    print("Example 1: Basic PDF Stitching")
    print("-" * 40)
    
    # Create stitcher instance
    stitcher = PDFStitcher()
    
    # Add files (these would be real files in practice)
    try:
        stitcher.add_pdf("document1.pdf")
        stitcher.add_pdf("document2.pdf")
        print(f"Added {stitcher.get_file_count()} files")
        
        # Save (would actually create PDF if files existed)
        # result = stitcher.save("combined.pdf")
        # print(f"Created: {result}")
        
    except FileNotFoundError:
        print("Note: This example requires actual PDF files")
    
    print()


def example_mixed_content() -> None:
    """Example: Mixing PDFs and images."""
    print("Example 2: Mixing PDFs and Images")
    print("-" * 40)
    
    try:
        # Use the convenience function
        input_files = [
            "report.pdf",
            "chart.png",
            "graph.jpg",
            "appendix.pdf"
        ]
        
        # This would work if the files existed
        # result = stitch_files(input_files, "final_report.pdf")
        # print(f"Combined {len(input_files)} files into: {result}")
        
        print(f"Would combine {len(input_files)} files:")
        for i, file_path in enumerate(input_files, 1):
            print(f"  {i}. {file_path}")
        
    except FileNotFoundError:
        print("Note: This example requires actual files")
    
    print()


def example_context_manager() -> None:
    """Example: Using context manager for automatic cleanup."""
    print("Example 3: Context Manager Usage")
    print("-" * 40)
    
    try:
        with PDFStitcher() as stitcher:
            stitcher.add_pdf("doc1.pdf")
            stitcher.add_image("image.jpg")
            stitcher.add_pdf("doc2.pdf")
            
            print(f"Files in stitcher: {stitcher.get_file_count()}")
            print("Files:", stitcher.get_file_list())
            
            # Context manager automatically cleans up temp files
            # result = stitcher.save("output.pdf")
        
        print("Context manager automatically cleaned up resources")
        
    except FileNotFoundError:
        print("Note: This example requires actual files")
    
    print()


def example_image_converter() -> None:
    """Example: Direct image conversion."""
    print("Example 4: Direct Image Conversion")
    print("-" * 40)
    
    converter = ImageConverter()
    
    # Show supported formats
    print("Supported image formats:")
    for fmt in sorted(converter.supported_formats):
        print(f"  {fmt}")
    
    # Test file type detection
    test_files = ["image.jpg", "document.pdf", "photo.png", "text.txt"]
    print("\nFile type detection:")
    for file_path in test_files:
        is_image = converter.is_image_file(file_path)
        print(f"  {file_path}: {'✓ Image' if is_image else '✗ Not an image'}")
    
    print()


def example_file_info() -> None:
    """Example: Getting file information."""
    print("Example 5: File Information")
    print("-" * 40)
    
    # This would work with real files
    try:
        # info = get_file_info("example.pdf")
        # print(f"File: {info['name']}")
        # print(f"Size: {info['size_formatted']}")
        # print(f"Extension: {info['extension']}")
        
        print("This example shows how to get file information")
        print("(requires actual files to work)")
        
    except FileNotFoundError:
        print("Note: This example requires actual files")
    
    print()


def example_error_handling() -> None:
    """Example: Proper error handling."""
    print("Example 6: Error Handling")
    print("-" * 40)
    
    stitcher = PDFStitcher()
    
    # Try to add non-existent file
    try:
        stitcher.add_pdf("nonexistent.pdf")
    except FileNotFoundError as e:
        print(f"Caught expected error: {e}")
    
    # Try to add wrong file type
    try:
        # Create a dummy text file for testing
        dummy_file = "test.txt"
        with open(dummy_file, 'w', encoding='utf-8') as f:
            f.write("dummy content")
        
        stitcher.add_pdf(dummy_file)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    finally:
        # Clean up
        if os.path.exists(dummy_file):
            os.unlink(dummy_file)
    
    # Try to stitch without files
    try:
        stitcher.save("empty.pdf")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    
    print()


def main() -> None:
    """Run all examples."""
    print("PDF Stitcher - Usage Examples")
    print("=" * 50)
    print()
    
    example_basic_stitching()
    example_mixed_content()
    example_context_manager()
    example_image_converter()
    example_file_info()
    example_error_handling()
    
    print("All examples completed!")
    print("\nTo run with real files:")
    print("1. Create some PDF and image files")
    print("2. Update the file paths in the examples")
    print("3. Run the examples again")


if __name__ == "__main__":
    main()
