import os
import gzip
import unittest
from utils.utilities import unzip_gzip_file

class TestUtilities(unittest.TestCase):

    def test_unzip_gzip_file(self):
        # Create a test gzip file
        test_content = b'Test content to gzip'
        test_gzip_file = 'test_file.gz'
        with gzip.open(test_gzip_file, 'wb') as f:
            f.write(test_content)

        # Unzip the test gzip file
        unzipped_file = 'unzipped_test_file.txt'
        unzip_gzip_file(test_gzip_file, unzipped_file)

        # Check if unzipped file content is the same as original content
        with open(unzipped_file, 'rb') as f:
            unzipped_content = f.read()
            self.assertEqual(test_content, unzipped_content)

        # Clean up the test files
        os.remove(test_gzip_file)
        os.remove(unzipped_file)