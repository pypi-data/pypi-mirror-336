# HPFC: High-Performance Folder Compare

A high-performance command-line tool for comparing directories and generating detailed reports on file differences.
This tool supports cross-platform operation (Windows, Linux, and macOS) and can efficiently handle large volumes of files and large file sizes.

## Features

- Compare files in two directories for content differences
- Detect and report three types of inconsistencies:
  - Files with different content
  - Missing files (present in dir1 but not in dir2)
  - Extra files (present in dir2 but not in dir1)
- Cross-platform support (Windows, Linux, and macOS)
- Uses chunked hash comparison algorithm for efficient handling of large files (up to tens of GB)
- Multi-process parallel processing for improved performance
- File and directory ignore patterns
- Detailed reports in both text and HTML formats
- Interactive progress bar with ETA display
- Handles tens or hundreds of thousands of files efficiently

## Installation

### Using pip

```bash
pip install hpfc-tool
```

> **Note:** The package name is `hpfc-tool` and the command-line tool is `hpfc`.

### From source

```bash
git clone https://github.com/yourusername/hpfc.git
cd hpfc
pip install .
```

## Usage

### Basic Usage

```bash
hpfc directory1 directory2
```

### Advanced Options

```bash
hpfc directory1 directory2 [options]
```

Options:
- `-c`, `--chunk-size`: Chunk size in bytes for comparing large files (default: 8MB)
- `-w`, `--workers`: Number of worker processes for parallel processing (default: CPU count)
- `-i`, `--ignore`: Patterns to ignore (can specify multiple)
- `-o`, `--output`: Save report to specified file (default: console output)
- `--html`: Generate an HTML report instead of text
- `--no-progress`: Disable progress bar display
- `-v`, `--version`: Show version information

### Examples

Compare two directories:
```bash
hpfc /path/to/dir1 /path/to/dir2
```

Ignore specific files or directories:
```bash
hpfc /path/to/dir1 /path/to/dir2 --ignore ".git" "*.log" "temp"
```

Adjust chunk size for large file comparison:
```bash
hpfc /path/to/dir1 /path/to/dir2 --chunk-size 16777216  # 16MB
```

Specify number of worker processes:
```bash
hpfc /path/to/dir1 /path/to/dir2 --workers 4
```

Save report to file:
```bash
hpfc /path/to/dir1 /path/to/dir2 --output report.txt
```

Generate HTML report:
```bash
hpfc /path/to/dir1 /path/to/dir2 --html --output report.html
```

### Exit Codes

- `0`: All files are identical
- `1`: There are different files, missing files, extra files, or error files

## Performance Considerations

- For large files (>8MB), the tool uses chunked hash comparison instead of full file loading to avoid memory overflow
- For small files, direct content comparison is used, which is generally faster than hash calculation
- The tool uses multi-process parallel processing for file comparison to utilize multi-core CPUs
- Performance priority: files are first compared by size, and only if sizes match are contents compared

## Running Tests

```bash
python -m unittest discover -s tests
```

To skip large file tests (which may take some time):
```bash
SKIP_LARGE_FILE_TEST=1 python -m unittest discover -s tests
```

## Project Structure

```
hpfc-tool/
├── src/
│   └── hpfc/
│       ├── __init__.py    # Package initialization
│       ├── core.py        # Core comparison functionality
│       └── cli.py         # Command-line interface
├── tests/
│   └── test_hpfc.py       # Test cases
├── setup.py               # Package setup
└── README.md              # Documentation
```

## Notes

- This tool is specifically designed for handling large volumes of files and large file sizes
- Binary and text files are compared in the same way (exact content comparison)
- Ignore patterns use simple substring matching, not wildcards or regular expressions
- HTML reports provide an interactive and visual representation of comparison results 