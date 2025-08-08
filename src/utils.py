"""Utility functions for PDF Stitcher."""

import os
from pathlib import Path
from typing import List


def validate_file_exists(file_path: str) -> None:
    """
    Validate that a file exists.

    Args:
        file_path: Path to the file to check

    Raises:
        FileNotFoundError: If the file doesn't exist
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError(f"Path is not a file: {file_path}")


def get_file_extension(file_path: str) -> str:
    """
    Get the file extension in lowercase.

    Args:
        file_path: Path to the file

    Returns:
        File extension in lowercase (including the dot)
    """
    return Path(file_path).suffix.lower()


def get_file_name(file_path: str) -> str:
    """
    Get the file name without extension.

    Args:
        file_path: Path to the file

    Returns:
        File name without extension
    """
    return Path(file_path).stem


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary.

    Args:
        directory_path: Path to the directory
    """
    os.makedirs(directory_path, exist_ok=True)


def filter_files_by_extension(
    file_paths: List[str], extensions: List[str]
) -> List[str]:
    """
    Filter a list of file paths by their extensions.

    Args:
        file_paths: List of file paths to filter
        extensions: List of extensions to keep (including dots, case-insensitive)

    Returns:
        Filtered list of file paths
    """
    extensions_lower = [ext.lower() for ext in extensions]
    return [
        file_path
        for file_path in file_paths
        if get_file_extension(file_path) in extensions_lower
    ]


def get_pdf_files(file_paths: List[str]) -> List[str]:
    """
    Filter a list to get only PDF files.

    Args:
        file_paths: List of file paths to filter

    Returns:
        List of PDF file paths
    """
    return filter_files_by_extension(file_paths, [".pdf"])


def get_image_files(file_paths: List[str]) -> List[str]:
    """
    Filter a list to get only image files.

    Args:
        file_paths: List of file paths to filter

    Returns:
        List of image file paths
    """
    image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif"]
    return filter_files_by_extension(file_paths, image_extensions)


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string
    """
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.1f} {size_names[i]}"


def get_file_info(file_path: str) -> dict:
    """
    Get information about a file.

    Args:
        file_path: Path to the file

    Returns:
        Dictionary with file information
    """
    validate_file_exists(file_path)

    stat = os.stat(file_path)

    return {
        "name": os.path.basename(file_path),
        "path": file_path,
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "extension": get_file_extension(file_path),
        "modified": stat.st_mtime,
    }
