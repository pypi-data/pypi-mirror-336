#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HPFC Core

A high-performance tool for comparing directories and files.
Supports cross-platform operation (Windows, Linux, macOS) and can efficiently
handle large volumes of files and large file sizes.
"""

import os
import sys
import hashlib
import time
import jinja2
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .__init__ import __version__


class ProgressBar:
    """Simple progress bar for console output"""

    def __init__(
        self, total: int, prefix: str = "", suffix: str = "", length: int = 50, fill: str = "█"
    ):
        """
        Initialize progress bar

        Args:
            total: Total number of items
            prefix: Prefix string
            suffix: Suffix string
            length: Bar length
            fill: Bar fill character
        """
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.iteration = 0
        self.start_time = time.time()
        self.last_update = 0
        self._print_progress()

    def update(self, iteration: Optional[int] = None) -> None:
        """Update progress bar"""
        if iteration is not None:
            self.iteration = iteration
        else:
            self.iteration += 1

        # Only update display every 0.1 seconds to avoid excessive printing
        current_time = time.time()
        if current_time - self.last_update >= 0.1 or self.iteration == self.total:
            self.last_update = current_time
            self._print_progress()

    def _print_progress(self) -> None:
        """Print the progress bar"""
        percent = "{0:.1f}".format(100 * (self.iteration / float(self.total)))
        filled_length = int(self.length * self.iteration // self.total)
        bar = self.fill * filled_length + "-" * (self.length - filled_length)

        # Calculate ETA
        if self.iteration > 0:
            elapsed = time.time() - self.start_time
            items_per_second = self.iteration / elapsed
            eta = (self.total - self.iteration) / items_per_second if items_per_second > 0 else 0
            eta_str = f"ETA: {int(eta // 60)}m {int(eta % 60)}s"
        else:
            eta_str = "ETA: --"

        # Create the progress line
        progress_line = (
            f"\r{self.prefix} |{bar}| {percent}% {self.iteration}/{self.total} "
            f"{eta_str} {self.suffix}"
        )

        # Print progress bar
        sys.stdout.write(progress_line)
        sys.stdout.flush()

        # Print new line on complete
        if self.iteration == self.total:
            elapsed = time.time() - self.start_time
            speed = self.total / elapsed if elapsed > 0 else 0
            print(f"\nCompleted in {elapsed:.2f}s ({speed:.2f} items/s)")


class DirectoryComparer:
    """Directory Comparison Tool Class"""

    def __init__(
        self,
        dir1: str,
        dir2: str,
        chunk_size: int = 8 * 1024 * 1024,  # 8MB chunk size
        max_workers: Optional[int] = None,
        ignore_patterns: List[str] = None,
        show_progress: bool = True,
    ):
        """
        Initialize the comparison tool

        Args:
            dir1: Path to the first directory
            dir2: Path to the second directory
            chunk_size: Size of chunks for file comparison, used for handling large files
            max_workers: Maximum number of worker processes for parallel processing,
                         None for CPU count
            ignore_patterns: List of file/directory patterns to ignore
            show_progress: Whether to show progress bar
        """
        self.dir1 = os.path.abspath(dir1)
        self.dir2 = os.path.abspath(dir2)
        self.chunk_size = chunk_size
        self.max_workers = max_workers
        self.ignore_patterns = ignore_patterns or []
        self.show_progress = show_progress

        # Comparison results
        self.different_files = []  # Files with different content
        self.missing_files = []  # Files present in dir1 but missing in dir2
        self.extra_files = []  # Files present in dir2 but not in dir1
        self.identical_files = []  # Files that are completely identical
        self.error_files = []  # Files that caused errors during comparison

        # Performance statistics
        self.total_files_processed = 0
        self.total_size_processed = 0
        self.start_time = None
        self.end_time = None

    def should_ignore(self, path: str) -> bool:
        """Check if a path should be ignored"""
        rel_path = os.path.basename(path)
        for pattern in self.ignore_patterns:
            if pattern in rel_path:
                return True
        return False

    def get_files_dict(self, directory: str) -> Dict[str, Path]:
        """
        Get a dictionary of all files in the directory with their relative and absolute paths

        Returns: {relative_path: Path_object}
        """
        files_dict = {}
        for root, _, files in os.walk(directory):
            if self.should_ignore(root):
                continue

            for file in files:
                if self.should_ignore(file):
                    continue

                full_path = os.path.join(root, file)
                # Calculate path relative to base_dir
                rel_path = os.path.relpath(full_path, directory)
                files_dict[rel_path] = Path(full_path)

        return files_dict

    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate SHA256 hash of a file

        For large files, read in chunks to avoid loading the entire file into memory
        """
        sha256_hash = hashlib.sha256()

        try:
            with open(file_path, "rb") as f:
                # Read file in chunks
                for byte_block in iter(lambda: f.read(self.chunk_size), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            self.error_files.append((str(file_path), str(e)))
            return None

    def compare_files(self, rel_path: str, file1: Path, file2: Path) -> bool:
        """
        Compare two files to determine if they are identical

        First compares file size, if different returns False
        Then compares file content or hash

        Returns: True if files are identical, False otherwise
        """
        try:
            # First compare file sizes
            if file1.stat().st_size != file2.stat().st_size:
                return False

            # For small files, direct content comparison may be faster
            if file1.stat().st_size < self.chunk_size:
                with open(file1, "rb") as f1, open(file2, "rb") as f2:
                    return f1.read() == f2.read()

            # For large files, compare hashes
            hash1 = self.calculate_file_hash(file1)
            hash2 = self.calculate_file_hash(file2)

            return hash1 == hash2
        except Exception as e:
            self.error_files.append((rel_path, str(e)))
            return False

    def process_file_comparison(self, rel_path: str, file1: Path, file2: Path) -> Tuple[str, bool]:
        """Process a single file comparison, can be called by parallel processor"""
        is_identical = self.compare_files(rel_path, file1, file2)
        file_size = file1.stat().st_size
        self.total_size_processed += file_size

        return rel_path, is_identical

    def compare(self) -> Dict:
        """
        Execute directory comparison

        Returns a dictionary containing comparison results
        """
        self.start_time = time.time()

        # Get file lists for both directories
        print(f"Scanning directory: {self.dir1}")
        files_dict1 = self.get_files_dict(self.dir1)
        print(f"Scanning directory: {self.dir2}")
        files_dict2 = self.get_files_dict(self.dir2)

        # Find files in dir1 that are missing in dir2
        self.missing_files = [f for f in files_dict1.keys() if f not in files_dict2]

        # Find files in dir2 that are not in dir1
        self.extra_files = [f for f in files_dict2.keys() if f not in files_dict1]

        # Find files present in both directories that need content comparison
        common_files = [f for f in files_dict1.keys() if f in files_dict2]
        self.total_files_processed = (
            len(common_files) + len(self.missing_files) + len(self.extra_files)
        )

        print(f"Starting comparison of {len(common_files)} common files...")

        # Use parallel processing to speed up file comparison
        if common_files:  # Only start parallel processing if there are common files
            # Create progress bar
            progress = None
            if self.show_progress:
                progress = ProgressBar(
                    len(common_files), prefix="Progress:", suffix="Complete", length=50
                )

            with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all comparison tasks to the process pool
                future_to_file = {
                    executor.submit(
                        self.compare_files, rel_path, files_dict1[rel_path], files_dict2[rel_path]
                    ): rel_path
                    for rel_path in common_files
                }

                # Collect results
                for i, future in enumerate(future_to_file):
                    rel_path = future_to_file[future]
                    try:
                        is_identical = future.result()
                        if is_identical:
                            self.identical_files.append(rel_path)
                        else:
                            self.different_files.append(rel_path)
                    except Exception as e:
                        self.error_files.append((rel_path, str(e)))

                    # Update progress bar
                    if progress:
                        progress.update(i + 1)
                    elif (i + 1) % 100 == 0 or (i + 1) == len(common_files):
                        # Fall back to simple progress output if no progress bar
                        print(f"Compared: {i + 1}/{len(common_files)} files")

        self.end_time = time.time()

        # Return comparison results
        return {
            "identical_files": self.identical_files,
            "different_files": self.different_files,
            "missing_files": self.missing_files,
            "extra_files": self.extra_files,
            "error_files": self.error_files,
            "total_files_processed": self.total_files_processed,
            "total_size_processed": self.total_size_processed,
            "time_elapsed": self.end_time - self.start_time,
        }

    def generate_text_report(self, results: Dict = None) -> str:
        """Generate a text comparison report"""
        if results is None:
            results = {
                "identical_files": self.identical_files,
                "different_files": self.different_files,
                "missing_files": self.missing_files,
                "extra_files": self.extra_files,
                "error_files": self.error_files,
                "total_files_processed": self.total_files_processed,
                "total_size_processed": self.total_size_processed,
                "time_elapsed": self.end_time - self.start_time if self.end_time else 0,
            }

        # Calculate processing speed
        speed = (
            results["total_size_processed"] / results["time_elapsed"]
            if results["time_elapsed"] > 0
            else 0
        )

        # Generate report
        report = [
            "=" * 80,
            "Folder Comparison Report",
            "=" * 80,
            f"Folder 1: {self.dir1}",
            f"Folder 2: {self.dir2}",
            f"Total files compared: {results['total_files_processed']}",
            f"Total data processed: {results['total_size_processed'] / (1024*1024):.2f} MB",
            f"Processing time: {results['time_elapsed']:.2f} seconds",
            f"Processing speed: {speed / (1024*1024):.2f} MB/s",
            "-" * 80,
            f"Identical files: {len(results['identical_files'])}",
            f"Files with different content: {len(results['different_files'])}",
            f"Missing files (in folder1 but not in folder2): {len(results['missing_files'])}",
            f"Extra files (in folder2 but not in folder1): {len(results['extra_files'])}",
            f"Error files: {len(results['error_files'])}",
        ]

        # Add detailed list of different files
        if results["different_files"]:
            report.extend(["-" * 80, "Files with different content:", "-" * 80])
            for file in sorted(results["different_files"]):
                report.append(f"  {file}")

        # Add list of missing files
        if results["missing_files"]:
            report.extend(["-" * 80, "Missing files (in folder1 but not in folder2):", "-" * 80])
            for file in sorted(results["missing_files"]):
                report.append(f"  {file}")

        # Add list of extra files
        if results["extra_files"]:
            report.extend(["-" * 80, "Extra files (in folder2 but not in folder1):", "-" * 80])
            for file in sorted(results["extra_files"]):
                report.append(f"  {file}")

        # Add list of error files
        if results["error_files"]:
            report.extend(["-" * 80, "Error files:", "-" * 80])
            for file, error in results["error_files"]:
                report.append(f"  {file}: {error}")

        # Add footer with links and author information
        report.extend([
            "=" * 80,
            f"Generated by HPFC - High-Performance Folder Compare v{__version__}",
            f"Author: Ethan Li",
            f"GitHub: https://github.com/ethan-li/hpfc",
            f"PyPI: https://pypi.org/project/hpfc-tool/",
            "=" * 80
        ])

        return "\n".join(report)

    def generate_html_report(self, results: Dict = None) -> str:
        """Generate an HTML comparison report"""
        if results is None:
            results = {
                "identical_files": self.identical_files,
                "different_files": self.different_files,
                "missing_files": self.missing_files,
                "extra_files": self.extra_files,
                "error_files": self.error_files,
                "total_files_processed": self.total_files_processed,
                "total_size_processed": self.total_size_processed,
                "time_elapsed": self.end_time - self.start_time if self.end_time else 0,
            }

        # Calculate processing speed
        speed = (
            results["total_size_processed"] / results["time_elapsed"]
            if results["time_elapsed"] > 0
            else 0
        )

        # Create template
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Folder Comparison Report</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    color: #333;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                }
                .summary {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .info-box {
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 15px;
                }
                .stats {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-bottom: 20px;
                }
                .stat-box {
                    flex: 1;
                    min-width: 150px;
                    background-color: #fff;
                    border-radius: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    padding: 15px;
                    text-align: center;
                }
                .details {
                    margin-top: 30px;
                }
                .section {
                    margin-bottom: 30px;
                }
                h1 {
                    color: #2c3e50;
                    margin: 0 0 10px 0;
                }
                h2 {
                    color: #3498db;
                    margin: 0 0 15px 0;
                    padding-bottom: 10px;
                    border-bottom: 1px solid #eee;
                }
                h3 {
                    color: #555;
                }
                .file-list {
                    background-color: #f8f9fa;
                    padding: 15px;
                    border-radius: 5px;
                    max-height: 300px;
                    overflow-y: auto;
                }
                .file-list ul {
                    list-style-type: none;
                    padding: 0;
                    margin: 0;
                }
                .file-list li {
                    padding: 5px 10px;
                    border-bottom: 1px solid #eee;
                    word-break: break-all;
                }
                .different {
                    background-color: #ffecb3;
                }
                .missing {
                    background-color: #ffcdd2;
                }
                .extra {
                    background-color: #c8e6c9;
                }
                .error {
                    background-color: #ffcdd2;
                    color: #d32f2f;
                }
                .timestamp {
                    font-size: 0.8em;
                    color: #777;
                    margin-top: 5px;
                }
                .stat-title {
                    font-size: 0.9em;
                    color: #555;
                    margin-bottom: 5px;
                }
                .stat-value{
                    font-size: 1.6em;
                    font-weight: bold;
                }
                .warning {
                    color: #e74c3c;
                }
                .success {
                    color: #27ae60;
                }
                .footer {
                    margin-top: 50px;
                    text-align: center;
                    padding: 20px;
                    color: #777;
                    font-size: 0.9em;
                    border-top: 1px solid #eee;
                }
                .footer a {
                    color: #3498db;
                    text-decoration: none;
                }
                .footer a:hover {
                    text-decoration: underline;
                }
                .project-links {
                    margin-top: 10px;
                    display: flex;
                    justify-content: center;
                    gap: 20px;
                }
                .project-link {
                    display: inline-flex;
                    align-items: center;
                    padding: 5px 10px;
                    border-radius: 4px;
                    background-color: #f8f9fa;
                    transition: background-color 0.2s ease;
                }
                .project-link:hover {
                    background-color: #e9ecef;
                }
                .project-link img {
                    margin-right: 5px;
                    width: 16px;
                    height: 16px;
                }
                @media (max-width: 768px) {
                    .summary {
                        grid-template-columns: 1fr;
                    }
                    .stats {
                        flex-direction: column;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Folder Comparison Report</h1>
                    <div class="timestamp">Generated on: {{ timestamp }}</div>
                </div>

                <div class="summary">
                    <div class="info-box">
                        <h3>Folder 1</h3>
                        <p>{{ dir1 }}</p>
                    </div>
                    <div class="info-box">
                        <h3>Folder 2</h3>
                        <p>{{ dir2 }}</p>
                    </div>
                </div>

                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-title">Total Files</div>
                        <div class="stat-value">{{ total_files }}</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-title">Identical Files</div>
                        <div class="stat-value
                            {% if identical_files_count == total_files %}success{% endif %}">
                            {{ identical_files_count }}
                        </div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-title">Different Files</div>
                        <div class="stat-value
                            {% if different_files_count > 0 %}warning{% endif %}">
                            {{ different_files_count }}
                        </div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-title">Missing Files</div>
                        <div class="stat-value{% if missing_files_count > 0 %}warning{% endif %}">
                            {{ missing_files_count }}
                        </div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-title">Extra Files</div>
                        <div class="stat-value{% if extra_files_count > 0 %}warning{% endif %}">
                            {{ extra_files_count }}
                        </div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-title">Error Files</div>
                        <div class="stat-value{% if error_files_count > 0 %}warning{% endif %}">
                            {{ error_files_count }}
                        </div>
                    </div>
                </div>

                <div class="info-box">
                    <h3>Performance Metrics</h3>
                    <p>Total data processed: {{ data_processed }} MB</p>
                    <p>Processing time: {{ time_elapsed }} seconds</p>
                    <p>Processing speed: {{ speed }} MB/s</p>
                </div>

                <div class="details">
                    {% if different_files %}
                    <div class="section">
                        <h2>Files with Different Content</h2>
                        <div class="file-list different">
                            <ul>
                            {% for file in different_files %}
                                <li>{{ file }}</li>
                            {% endfor %}
                            </ul>
                        </div>
                    </div>
                    {% endif %}

                    {% if missing_files %}
                    <div class="section">
                        <h2>Missing Files (in folder1 but not in folder2)</h2>
                        <div class="file-list missing">
                            <ul>
                            {% for file in missing_files %}
                                <li>{{ file }}</li>
                            {% endfor %}
                            </ul>
                        </div>
                    </div>
                    {% endif %}

                    {% if extra_files %}
                    <div class="section">
                        <h2>Extra Files (in folder2 but not in folder1)</h2>
                        <div class="file-list extra">
                            <ul>
                            {% for file in extra_files %}
                                <li>{{ file }}</li>
                            {% endfor %}
                            </ul>
                        </div>
                    </div>
                    {% endif %}

                    {% if error_files %}
                    <div class="section">
                        <h2>Error Files</h2>
                        <div class="file-list error">
                            <ul>
                            {% for file, error in error_files %}
                                <li>{{ file }}: {{ error }}</li>
                            {% endfor %}
                            </ul>
                        </div>
                    </div>
                    {% endif %}
                </div>
                
                <div class="footer">
                    <p>Generated by <strong>{{ repo_name }}</strong> v{{ version }}</p>
                    <p>Created by <strong>{{ author }}</strong></p>
                    <div class="project-links">
                        <a href="{{ github_url }}" target="_blank" class="project-link">
                            <img src="https://github.com/favicon.ico" alt="GitHub"> GitHub Project
                        </a>
                        <a href="{{ pypi_url }}" target="_blank" class="project-link">
                            <img src="https://pypi.org/static/images/favicon.ico" alt="PyPI"> PyPI Package
                        </a>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Prepare template data
        template_data = {
            "dir1": self.dir1,
            "dir2": self.dir2,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_files": results["total_files_processed"],
            "identical_files_count": len(results["identical_files"]),
            "different_files_count": len(results["different_files"]),
            "missing_files_count": len(results["missing_files"]),
            "extra_files_count": len(results["extra_files"]),
            "error_files_count": len(results["error_files"]),
            "data_processed": f"{results['total_size_processed'] / (1024*1024):.2f}",
            "time_elapsed": f"{results['time_elapsed']:.2f}",
            "speed": f"{speed / (1024*1024):.2f}",
            "different_files": sorted(results["different_files"]),
            "missing_files": sorted(results["missing_files"]),
            "extra_files": sorted(results["extra_files"]),
            "error_files": results["error_files"],
            "repo_name": "HPFC - High-Performance Folder Compare",
            "github_url": "https://github.com/ethan-li/hpfc",
            "pypi_url": "https://pypi.org/project/hpfc-tool/",
            "version": __version__,
            "author": "Ethan Li"
        }

        # Render template
        template = jinja2.Template(template_str)
        return template.render(**template_data)
