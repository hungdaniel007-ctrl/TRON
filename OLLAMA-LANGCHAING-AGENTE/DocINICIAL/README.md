# Documentation Indexer System

A robust and production-ready system for extracting hierarchical titles from Markdown documents and verifying the integrity of the generated index.

## Overview

The Documentation Indexer System consists of two main components:

1. **Extract Titles (`extract_titles.py`)**: Extracts hierarchical titles from Markdown files and creates an index with their positions and levels.
2. **Verify Index (`verify_index.py`)**: Verifies the coherence and correctness of the generated index against the original Markdown content.

## Features

- **Hierarchical Title Extraction**: Accurately identifies and indexes titles at different levels (H1-H6) in Markdown documents
- **Content Filtering**: Filters titles based on content length to ensure meaningful sections
- **Empty Header Handling**: Properly handles empty headers followed by titles on subsequent lines
- **Code Block Awareness**: Ignores headers within code blocks
- **Comprehensive Verification**: Checks both correctness (titles exist in original document) and coherence (titles represent substantial content)
- **Detailed Logging**: Comprehensive logging with configurable log levels
- **Error Handling**: Robust error handling with informative messages
- **Flexible Input/Output**: Command-line interface for flexible usage

## Prerequisites

- Python 3.7+
- Standard Python libraries (no external dependencies required)

## Installation

### Quick Setup

Run the setup script to create a virtual environment and install dependencies:

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### Manual Setup

1. Create a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies (if any):
```bash
pip install -r requirements.txt
```

## Usage

### Extract Titles

To extract titles from a Markdown file:

```bash
python doc_indexer/extract_titles.py -i input.md -o index.json
```

Additional options:
```bash
# With custom log file and debug output
python doc_indexer/extract_titles.py -i input.md -o index.json --log-file custom.log --debug

# Full usage
python doc_indexer/extract_titles.py -h
```

### Verify Index

To verify the generated index against the original Markdown:

```bash
python doc_indexer/verify_index.py -m input.md -i index.json
```

Additional options:
```bash
# With custom log file and debug output
python doc_indexer/verify_index.py -m input.md -i index.json --log-file custom.log --debug

# Full usage
python doc_indexer/verify_index.py -h
```

### Using Wrapper Scripts (Recommended)

For convenience, use the provided wrapper scripts that automatically activate the virtual environment:

```bash
# Extract titles
./run_extract.sh -i input.md -o index.json

# Verify index
./run_verify.sh -m input.md -i index.json
```

## Command-Line Options

### Extract Titles (`extract_titles.py`)

```
usage: extract_titles.py [-h] -i INPUT -o OUTPUT [--log-file LOG_FILE] [--debug]

Extract hierarchical titles from Markdown files and create an index.

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input Markdown file path
  -o OUTPUT, --output OUTPUT
                        Output JSON index file path
  --log-file LOG_FILE   Log file path (default: logs/extract_titles.log)
  --debug               Enable debug logging
```

### Verify Index (`verify_index.py`)

```
usage: verify_index.py [-h] -m MARKDOWN -i INDEX [--log-file LOG_FILE] [--debug]

Verify the coherence and correctness of a documentation index.

options:
  -h, --help            show this help message and exit
  -m MARKDOWN, --markdown MARKDOWN
                        Input Markdown file path
  -i INDEX, --index INDEX
                        Index JSON file path
  --log-file LOG_FILE   Log file path (default: logs/verify_index.log)
  --debug               Enable debug logging
```

## Output Format

The extracted titles are saved in JSON format with the following structure:

```json
[
  {
    "addr": "1.1",
    "title": "Main Section Title",
    "line": 5,
    "level": 1
  },
  {
    "addr": "2.1",
    "title": "Subsection Title",
    "line": 12,
    "level": 2
  }
]
```

Where:
- `addr`: Hierarchical address (Level.Position)
- `title`: The title text
- `line`: Line number in the original document
- `level`: Header level (1-6)

## Verification Process

The verification process performs two types of checks:

1. **Correctness Check**: Ensures each indexed title actually exists in the original Markdown document
2. **Coherence Check**: Verifies that each title represents a substantial content section (minimum 2 content lines)

Issues found during verification are logged with detailed information about the problem and location.

## Logging

Both scripts provide comprehensive logging with the following levels:
- INFO: General operation information
- DEBUG: Detailed processing information (when enabled)
- WARNING: Issues found during processing
- ERROR: Errors that prevent successful completion

Log files are created in the `logs/` directory by default.

## Integration with Documentation Workflow

The recommended workflow is:

1. Extract titles from your Markdown documentation:
   ```bash
   python doc_indexer/extract_titles.py -i documentation.md -o index.json
   ```

2. Verify the generated index:
   ```bash
   python doc_indexer/verify_index.py -m documentation.md -i index.json
   ```

3. Use the index for navigation, search, or other documentation tools

## Error Handling

The system handles various error conditions gracefully:
- Missing input files
- Invalid Markdown formatting
- I/O errors
- Malformed JSON output

All errors are logged with detailed information to aid troubleshooting.

## Production Considerations

- The system is designed for production use with comprehensive error handling
- Logging provides detailed operational information
- Memory usage scales linearly with document size
- Processing time is proportional to document length

## Troubleshooting

### Common Issues

1. **File not found errors**: Ensure input file paths are correct and files exist
2. **Permission errors**: Check file permissions for input/output files and log directory
3. **Memory issues with large files**: Process large files in chunks if needed

### Debugging

Enable debug logging with the `--debug` flag to get detailed processing information:

```bash
python doc_indexer/extract_titles.py -i input.md -o index.json --debug
```

## Validation Technique for Large Documents

For large documentation files, it's inefficient to read the entire document to validate the index. The system includes a sampling validation technique that allows verification of index accuracy without consuming excessive resources:

```bash
# Example of validating index against original document using sampling
./validate_samples.sh
```

This script randomly selects entries from the index and verifies that the line numbers correspond to the correct titles in the original document. This approach:

- Validates index accuracy without reading the entire document
- Efficiently handles large files (tested with 277,000+ line documents)
- Provides confidence in index integrity with minimal resource usage
- Demonstrates the correspondence between indexed line numbers and actual content

The validation technique is particularly useful for production environments where:

1. Documents are extremely large
2. Token consumption needs to be minimized
3. Verification needs to be performed efficiently
4. Resource usage must be optimized

## License

MIT License - See LICENSE file for details.