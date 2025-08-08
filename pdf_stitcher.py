#!/usr/bin/env python3
"""Command-line interface for PDF Stitcher."""
import sys
import os
import click
# Add src to path for imports

from src.pdf_stitcher import PDFStitcher, stitch_files
from src.utils import validate_file_exists, get_file_info


@click.command()
@click.option(
    '--input', '-i',
    multiple=True,
    required=True,
    help='Input files (PDFs and/or images). Can be specified multiple times.'
)
@click.option(
    '--output', '-o',
    required=True,
    help='Output PDF file path.'
)
@click.option(
    '--verbose', '-v',
    is_flag=True,
    help='Enable verbose output.'
)
@click.option(
    '--dry-run',
    is_flag=True,
    help='Show what would be processed without actually creating the output.'
)
def main(input: tuple, output: str, verbose: bool, dry_run: bool) -> None:  # pylint: disable=redefined-builtin
    """
    PDF Stitcher - Combine multiple PDFs and images into a single PDF.
    
    Examples:
    
        # Stitch multiple PDFs
        python pdf_stitcher.py -i file1.pdf -i file2.pdf -o combined.pdf
        
        # Combine PDFs and images
        python pdf_stitcher.py -i document.pdf -i image.jpg -o result.pdf
        
        # Use wildcards (shell expansion)
        python pdf_stitcher.py -i *.pdf -o combined.pdf
    """
    input_files = list(input)
    
    if verbose:
        click.echo("PDF Stitcher - Starting processing...")
        click.echo(f"Input files: {len(input_files)}")
        click.echo(f"Output file: {output}")
    
    # Validate input files
    validated_files = []
    total_size = 0
    
    for file_path in input_files:
        try:
            validate_file_exists(file_path)
            file_info = get_file_info(file_path)
            validated_files.append(file_path)
            total_size += file_info['size']
            
            if verbose:
                click.echo(f"  ✓ {file_info['name']} ({file_info['size_formatted']})")
                
        except (FileNotFoundError, ValueError) as e:
            click.echo(f"  ✗ Error with {file_path}: {e}", err=True)
            sys.exit(1)
    
    if not validated_files:
        click.echo("No valid files to process.", err=True)
        sys.exit(1)
    
    if verbose:
        from src.utils import format_file_size
        click.echo(f"Total input size: {format_file_size(total_size)}")
    
    # Dry run mode
    if dry_run:
        click.echo("\nDry run mode - would process:")
        for i, file_path in enumerate(validated_files, 1):
            file_info = get_file_info(file_path)
            click.echo(f"  {i}. {file_info['name']} ({file_info['extension']})")
        click.echo(f"\nWould create: {output}")
        return
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        if verbose:
            click.echo(f"Created output directory: {output_dir}")
    
    # Process files
    try:
        if verbose:
            click.echo("\nProcessing files...")
        
        result_path = stitch_files(validated_files, output)
        
        # Get output file info
        output_info = get_file_info(result_path)
        
        click.echo(f"✓ Successfully created: {result_path}")
        if verbose:
            click.echo(f"  Output size: {output_info['size_formatted']}")
            click.echo(f"  Pages combined from {len(validated_files)} files")
        
    except (OSError, RuntimeError) as e:
        click.echo(f"✗ Error during processing: {e}", err=True)
        sys.exit(1)


@click.group()
def cli() -> None:
    """PDF Stitcher CLI - Advanced operations."""


@cli.command()
@click.argument('files', nargs=-1, required=True)
def info(files: tuple) -> None:
    """Show information about PDF and image files."""
    for file_path in files:
        try:
            file_info = get_file_info(file_path)
            click.echo(f"\nFile: {file_info['name']}")
            click.echo(f"  Path: {file_info['path']}")
            click.echo(f"  Size: {file_info['size_formatted']}")
            click.echo(f"  Type: {file_info['extension']}")
            
            # Additional info for PDFs
            if file_info['extension'] == '.pdf':
                try:
                    from pypdf import PdfReader
                    reader = PdfReader(file_path)
                    click.echo(f"  Pages: {len(reader.pages)}")
                except (OSError, RuntimeError) as e:
                    click.echo(f"  Pages: Unable to read ({e})")
            
        except (OSError, RuntimeError) as e:
            click.echo(f"✗ Error reading {file_path}: {e}", err=True)


@cli.command()
@click.argument('directory')
@click.option('--output', '-o', default='combined.pdf', help='Output filename')
@click.option('--pattern', '-p', default='*', help='File pattern to match')
def stitch_directory(directory: str, output: str, pattern: str) -> None:
    """Stitch all PDFs and images in a directory."""
    import glob
    
    if not os.path.isdir(directory):
        click.echo(f"Error: {directory} is not a directory", err=True)
        sys.exit(1)
    
    # Find files matching pattern
    search_pattern = os.path.join(directory, pattern)
    files = glob.glob(search_pattern)
    
    if not files:
        click.echo(f"No files found matching pattern: {search_pattern}", err=True)
        sys.exit(1)
    
    # Filter for supported files
    supported_files = []
    stitcher = PDFStitcher()
    
    for file_path in sorted(files):
        try:
            if file_path.lower().endswith('.pdf') or stitcher.image_converter.is_image_file(file_path):
                supported_files.append(file_path)
        except (OSError, ValueError):
            pass
    
    if not supported_files:
        click.echo("No supported files (PDF or images) found", err=True)
        sys.exit(1)
    
    click.echo(f"Found {len(supported_files)} files to stitch:")
    for file_path in supported_files:
        click.echo(f"  - {os.path.basename(file_path)}")
    
    # Stitch files
    try:
        output_path = os.path.join(directory, output)
        result_path = stitch_files(supported_files, output_path)
        click.echo(f"✓ Successfully created: {result_path}")
    except (OSError, RuntimeError) as e:
        click.echo(f"✗ Error during stitching: {e}", err=True)
        sys.exit(1)


if __name__ == '__main__':
    # For backwards compatibility, check if using subcommands
    if len(sys.argv) > 1 and sys.argv[1] in ['info', 'stitch-directory']:
        cli()
    else:
        # Use main command - Click handles arguments automatically
        main()  # pylint: disable=no-value-for-parameter
