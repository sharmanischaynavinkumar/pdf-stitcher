"""Setup script for PDF Stitcher."""
from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    requirements = requirements_path.read_text().strip().split('\n')

setup(
    name="pdf-stitcher",
    version="1.0.0",
    author="PDF Stitcher Team",
    author_email="",
    description="A Python application to combine multiple PDFs and images into a single PDF document",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pdf-stitcher",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=8.0.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "pdf-stitcher=pdf_stitcher:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
