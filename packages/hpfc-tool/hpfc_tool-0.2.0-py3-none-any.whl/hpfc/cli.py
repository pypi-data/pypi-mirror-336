#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HPFC CLI

Command line interface for the HPFC tool.
"""

import os
import sys
import argparse
from .core import DirectoryComparer
from .__init__ import __version__


def main():
    """Main function, handles command line arguments and executes comparison"""
    parser = argparse.ArgumentParser(
        description="Compare files in two folders and generate a report."
    )
    parser.add_argument("dir1", help="Path to the first folder")
    parser.add_argument("dir2", help="Path to the second folder")
    parser.add_argument(
        "-c",
        "--chunk-size",
        type=int,
        default=8 * 1024 * 1024,  # Default 8MB
        help="Chunk size in bytes for comparing large files",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=None,
        help="Number of worker processes for parallel processing, " "defaults to CPU count",
    )
    parser.add_argument(
        "-i", "--ignore", nargs="+", default=[], help="Patterns to ignore (can specify multiple)"
    )
    parser.add_argument(
        "-o", "--output", help="Save report to the specified file (defaults to console output)"
    )
    parser.add_argument(
        "--html", action="store_true", help="Generate an HTML report instead of text"
    )
    parser.add_argument("--no-progress", action="store_true", help="Disable progress bar display")
    parser.add_argument(
        "-v", "--version", action="version", version=f"hpfc {__version__}"
    )

    args = parser.parse_args()

    # Validate directories
    if not os.path.isdir(args.dir1):
        print(f"Error: Folder does not exist - {args.dir1}")
        return 1

    if not os.path.isdir(args.dir2):
        print(f"Error: Folder does not exist - {args.dir2}")
        return 1

    # Create the comparer and execute comparison
    comparer = DirectoryComparer(
        args.dir1,
        args.dir2,
        chunk_size=args.chunk_size,
        max_workers=args.workers,
        ignore_patterns=args.ignore,
        show_progress=not args.no_progress,
    )

    results = comparer.compare()

    # Generate the report
    if args.html:
        report = comparer.generate_html_report(results)
    else:
        report = comparer.generate_text_report(results)

    # Output the report
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print(report)

    # Return non-zero exit code if any differences, missing files, extra files
    # or errors
    has_differences = (
        bool(results["different_files"])
        or bool(results["missing_files"])
        or bool(results["extra_files"])
        or bool(results["error_files"])
    )
    if has_differences:
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
