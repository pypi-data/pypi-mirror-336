#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
HPFC Test Module

Tests for various comparison scenarios including:
- Identical files
- Files with different content
- Missing files
- Extra files
- Large file comparison
"""

import os
import random
import shutil
import sys
import tempfile
import unittest

# Add parent directory to path so we can import the package
# This is common in test files and an acceptable exception to PEP 8 E402
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# pylint: disable=wrong-import-position
from src.hpfc.core import DirectoryComparer  # noqa: E402


class TestDirectoryComparer(unittest.TestCase):
    """Test functionality of DirectoryComparer class"""

    def setUp(self):
        """Create test directories and files"""
        # Create two temporary directories for testing
        self.test_dir1 = tempfile.mkdtemp(prefix="test_dir1_")
        self.test_dir2 = tempfile.mkdtemp(prefix="test_dir2_")

        # Create test subdirectories
        self.sub_dir1 = os.path.join(self.test_dir1, "subdir")
        self.sub_dir2 = os.path.join(self.test_dir2, "subdir")
        os.makedirs(self.sub_dir1, exist_ok=True)
        os.makedirs(self.sub_dir2, exist_ok=True)

        # Create identical files
        self.create_file(os.path.join(self.test_dir1, "same_file.txt"), "Hello, World!")
        self.create_file(os.path.join(self.test_dir2, "same_file.txt"), "Hello, World!")

        # Create files with different content
        self.create_file(os.path.join(self.test_dir1, "different_file.txt"), "Content A")
        self.create_file(os.path.join(self.test_dir2, "different_file.txt"), "Content B")

        # Create file only in dir1
        self.create_file(os.path.join(self.test_dir1, "only_in_dir1.txt"), "Only in dir1")

        # Create file only in dir2
        self.create_file(os.path.join(self.test_dir2, "only_in_dir2.txt"), "Only in dir2")

        # Create identical files in subdirectories
        self.create_file(os.path.join(self.sub_dir1, "sub_same.txt"), "Same in subdir")
        self.create_file(os.path.join(self.sub_dir2, "sub_same.txt"), "Same in subdir")

        # Create files with different content in subdirectories
        self.create_file(os.path.join(self.sub_dir1, "sub_diff.txt"), "Different A")
        self.create_file(os.path.join(self.sub_dir2, "sub_diff.txt"), "Different B")

    def tearDown(self):
        """Clean up test directories"""
        shutil.rmtree(self.test_dir1, ignore_errors=True)
        shutil.rmtree(self.test_dir2, ignore_errors=True)

    def create_file(self, path, content):
        """Create a file with specified content"""
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def create_large_file(self, path, size_mb):
        """Create a large file of specified size in MB"""
        # Write 1MB at a time
        chunk_size = 1024 * 1024
        with open(path, "wb") as f:
            for _ in range(size_mb):
                # Generate random data
                data = bytes([random.randint(0, 255) for _ in range(chunk_size)])
                f.write(data)

    def test_basic_comparison(self):
        """Test basic file comparison functionality"""
        comparer = DirectoryComparer(self.test_dir1, self.test_dir2)
        results = comparer.compare()

        # Check results
        self.assertEqual(
            len(results["identical_files"]), 2
        )  # same_file.txt and subdir/sub_same.txt
        self.assertEqual(
            len(results["different_files"]), 2
        )  # different_file.txt and subdir/sub_diff.txt
        self.assertEqual(len(results["missing_files"]), 1)  # only_in_dir1.txt
        self.assertEqual(len(results["extra_files"]), 1)  # only_in_dir2.txt

        # Check specific filenames
        self.assertIn("same_file.txt", results["identical_files"])
        self.assertIn(os.path.join("subdir", "sub_same.txt"), results["identical_files"])

        self.assertIn("different_file.txt", results["different_files"])
        self.assertIn(os.path.join("subdir", "sub_diff.txt"), results["different_files"])

        self.assertIn("only_in_dir1.txt", results["missing_files"])
        self.assertIn("only_in_dir2.txt", results["extra_files"])

    def test_empty_directories(self):
        """Test comparison of empty directories"""
        # Create two empty directories
        empty_dir1 = tempfile.mkdtemp(prefix="empty1_")
        empty_dir2 = tempfile.mkdtemp(prefix="empty2_")

        try:
            comparer = DirectoryComparer(empty_dir1, empty_dir2)
            results = comparer.compare()

            # Check results - all lists should be empty
            self.assertEqual(len(results["identical_files"]), 0)
            self.assertEqual(len(results["different_files"]), 0)
            self.assertEqual(len(results["missing_files"]), 0)
            self.assertEqual(len(results["extra_files"]), 0)
        finally:
            # Clean up
            shutil.rmtree(empty_dir1, ignore_errors=True)
            shutil.rmtree(empty_dir2, ignore_errors=True)

    def test_identical_directories(self):
        """Test comparison of identical directories"""
        # Create two identical directories
        temp_dir = tempfile.mkdtemp(prefix="identical_")
        clone_dir = tempfile.mkdtemp(prefix="clone_")

        try:
            # Create some files and subdirectories
            os.makedirs(os.path.join(temp_dir, "subdir"))
            self.create_file(os.path.join(temp_dir, "file1.txt"), "Content 1")
            self.create_file(os.path.join(temp_dir, "file2.txt"), "Content 2")
            self.create_file(os.path.join(temp_dir, "subdir", "file3.txt"), "Content 3")

            # Copy to clone directory
            shutil.rmtree(clone_dir)  # Clear first
            shutil.copytree(temp_dir, clone_dir)

            comparer = DirectoryComparer(temp_dir, clone_dir)
            results = comparer.compare()

            # Check results - all files should be identical
            self.assertEqual(len(results["identical_files"]), 3)  # 3 identical files
            self.assertEqual(len(results["different_files"]), 0)  # No different files
            self.assertEqual(len(results["missing_files"]), 0)  # No missing files
            self.assertEqual(len(results["extra_files"]), 0)  # No extra files
        finally:
            # Clean up
            shutil.rmtree(temp_dir, ignore_errors=True)
            shutil.rmtree(clone_dir, ignore_errors=True)

    def test_ignore_patterns(self):
        """Test pattern ignoring functionality"""
        comparer = DirectoryComparer(
            self.test_dir1, self.test_dir2, ignore_patterns=["only_in_dir1", "only_in_dir2"]
        )
        results = comparer.compare()

        # Should have ignored files that only exist in one directory
        self.assertEqual(len(results["missing_files"]), 0)
        self.assertEqual(len(results["extra_files"]), 0)

        # Other files should still be compared normally
        self.assertEqual(len(results["identical_files"]), 2)
        self.assertEqual(len(results["different_files"]), 2)

    @unittest.skipIf(os.environ.get("SKIP_LARGE_FILE_TEST"), "Skipping large file test")
    def test_large_file_comparison(self):
        """Test large file comparison functionality"""
        # Create smaller "large" files for unit testing (10MB)
        large_file1 = os.path.join(self.test_dir1, "large_file_same.bin")
        large_file2 = os.path.join(self.test_dir2, "large_file_same.bin")

        # Create two identical large files
        self.create_large_file(large_file1, 10)  # 10MB
        shutil.copy(large_file1, large_file2)

        # Create two different large files
        large_file3 = os.path.join(self.test_dir1, "large_file_diff.bin")
        large_file4 = os.path.join(self.test_dir2, "large_file_diff.bin")
        self.create_large_file(large_file3, 10)  # 10MB
        self.create_large_file(large_file4, 10)  # 10MB different content

        comparer = DirectoryComparer(self.test_dir1, self.test_dir2)
        results = comparer.compare()

        # Check results - large files should be correctly compared
        self.assertIn("large_file_same.bin", results["identical_files"])
        self.assertIn("large_file_diff.bin", results["different_files"])


class TestDirectoryComparerReport(unittest.TestCase):
    """Test report generation functionality"""

    def setUp(self):
        """Create test directories and mock results"""
        self.test_dir1 = "/path/to/dir1"  # Mock path, doesn't need to exist
        self.test_dir2 = "/path/to/dir2"

        # Create mock comparison results
        self.mock_results = {
            "identical_files": ["file1.txt", "file2.txt"],
            "different_files": ["diff1.txt", "diff2.txt"],
            "missing_files": ["missing1.txt"],
            "extra_files": ["extra1.txt", "extra2.txt"],
            "error_files": [("error1.txt", "Permission denied")],
            "total_files_processed": 7,
            "total_size_processed": 1024 * 1024 * 10,  # 10MB
            "time_elapsed": 2.5,
        }

    def test_text_report_generation(self):
        """Test text report generation"""
        comparer = DirectoryComparer(self.test_dir1, self.test_dir2)

        # Set attributes for report generation
        comparer.dir1 = self.test_dir1
        comparer.dir2 = self.test_dir2

        report = comparer.generate_text_report(self.mock_results)

        # Check report contains all necessary information
        self.assertIn(self.test_dir1, report)
        self.assertIn(self.test_dir2, report)
        self.assertIn("Total files compared: 7", report)
        self.assertIn("Identical files: 2", report)
        self.assertIn("Files with different content: 2", report)
        self.assertIn("Missing files", report)
        self.assertIn("Extra files", report)
        self.assertIn("diff1.txt", report)
        self.assertIn("missing1.txt", report)
        self.assertIn("extra1.txt", report)
        self.assertIn("error1.txt", report)
        self.assertIn("Permission denied", report)

    def test_html_report_generation(self):
        """Test HTML report generation"""
        comparer = DirectoryComparer(self.test_dir1, self.test_dir2)

        # Set attributes for report generation
        comparer.dir1 = self.test_dir1
        comparer.dir2 = self.test_dir2

        report = comparer.generate_html_report(self.mock_results)

        # Check HTML report contains all necessary information
        self.assertIn(self.test_dir1, report)
        self.assertIn(self.test_dir2, report)
        self.assertIn("Total Files", report)
        self.assertIn("Identical Files", report)
        self.assertIn("Different Files", report)
        self.assertIn("Missing Files", report)
        self.assertIn("Extra Files", report)
        self.assertIn("diff1.txt", report)
        self.assertIn("missing1.txt", report)
        self.assertIn("extra1.txt", report)
        self.assertIn("error1.txt", report)
        self.assertIn("Permission denied", report)

        # Check HTML structure
        self.assertIn("<!DOCTYPE html>", report)
        self.assertIn("<html>", report)
        self.assertIn("<head>", report)
        self.assertIn("<body>", report)
        self.assertIn("<style>", report)
        self.assertIn("<div", report)
        self.assertIn("</div>", report)
        self.assertIn("</html>", report)


if __name__ == "__main__":
    unittest.main()
