import os
import pytest
import unittest
from unittest.mock import patch
from pathlib import Path
from cobra import Model
from utils.data_io import load_arabidopsis_model, download_file, get_proteome

class TestDataIO(unittest.TestCase):

	def test_download_file(self):
		url = "https://www.ebi.ac.uk/biomodels/services/download/get-files/MODEL1507180028/2/MODEL1507180028_url.xml"
		directory = "../models"
		filename = "arabidopsis_model.xml"
		download_file(url, directory, filename)

	def test_load_arabidopsis_model(self):
		model = load_arabidopsis_model()
		assert model is not None
		assert isinstance(model, Model)
	def test_get_proteome_valid_input(self, tmpdir):
        # Create a temporary directory for the test
		directory = tmpdir.mkdir("test_out")
        # Create a mock download_file function
		with patch('your_module.download_file') as mock_download_file:
			mock_download_file.return_value = None

			# Call the function with valid input
			get_proteome("http://example.com/proteome.gz", str(directory), "test.gz")

            # Check that the download_file function was called with the correct arguments
			mock_download_file.assert_called_once_with("http://example.com/proteome.gz", str(directory), "test.gz")

            # Check that the zip file was created in the correct directory
			assert os.path.isfile(os.path.join(str(directory), "test.gz"))

            # Check that the unzipped file was created in the correct directory
			assert os.path.isfile(os.path.join(str(directory), "test"))

	def test_get_proteome_invalid_input(self):
        # Call the function with invalid input
		with pytest.raises(ValueError):
			get_proteome("http://example.com/proteome.gz", "invalid_directory", "test.gz")