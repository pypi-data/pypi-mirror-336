from setuptools import setup, find_packages

setup(
    name="pdf-section-parser",
    version="0.1.5",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Metadata
    author="Tamara Orlich",
    author_email="tamara.orlich@borah.agency", 
    description="A multilingual PDF parser that detects and extracts headers, body, and footers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="AGPL-3.0",
    
    # Dependencies
    python_requires=">=3.8",
    install_requires=[
        "pymupdf>=1.24.0",
        "pymupdf4llm>=0.0.17",
        "tqdm>=4.65.0"
    ],
    
    # Additional files
    package_data={
        "pdf_section_parser": ["py.typed"],
    },
    include_package_data=True,
    zip_safe=False,
    
    # Entry points for command-line usage
    entry_points={
        "console_scripts": [
            "pdf-section-parser=pdf_section_parser.cli.main:main",
        ],
    },
    
    # Project URLs
    project_urls={
        "Source": "https://github.com/BorahLabs/pdf_parser_with_header_footer/",
        "Bug Tracker": "https://github.com/BorahLabs/pdf_parser_with_header_footer/issues",
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: General",
        "Topic :: Scientific/Engineering :: Image Processing",
    ],
    
    # Keywords for PyPI
    keywords="pdf, parser, multilingual, text-extraction, document-processing, header-footer-detection",
)