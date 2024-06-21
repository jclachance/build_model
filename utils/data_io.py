import cobra
import os
import requests

from utils.utilities import check_directory_existence, unzip_gzip_file

def download_file(url: str, directory: str, filename: str):
    """
    Downloads a file from the given URL and saves it to the specified directory with the given filename.

    Parameters:
        url (str): The URL of the file to download.
        directory (str): The directory where the file will be saved. If the directory does not exist, it will be created.
        filename (str): The name of the file to be saved.

    Returns:
        None

    Raises:
        None

    Prints:
        - "File downloaded successfully: {filepath}" if the file is downloaded successfully.
        - "Failed to download the file. Status code: {response.status_code}" if the request fails.
    """
    # Create the directory if it doesn't exist
    check_directory_existence(directory)

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Save the response content to a file in the directory
        filepath = os.path.join(directory, filename)
        with open(filepath, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully: {filepath}")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")

def load_arabidopsis_model(path: str='../models/arabidopsis_model.xml') -> cobra.Model:
    """
    Load an Arabidopsis model from an SBML file.

    Args:
        path (str): The path to the SBML file. Defaults to '../models/arabidopsis_model.xml'.

    Returns:
        cobra.Model: The loaded Arabidopsis model.
    """
    return cobra.io.read_sbml_model(path)

def get_proteome(url:str, directory:str,filename:str):
    """
    Given a url, downloads a proteome from the NCBI FTP server and saves it to the specified directory.

    Args:
        url (str): The URL of the proteome file. 
        directory (str): The directory where the proteome file will be saved.
        filename (str): The name of the proteome file..

    Returns:
        None

    Raises:
        None
    """
    download_file(url, directory, filename)
    zip_filepath = os.path.join(directory, filename)
    unzipped_filepath = os.path.join(directory, filename.replace('.gz', ''))
    unzip_gzip_file(zip_filepath, unzipped_filepath)
    