import gzip
import os
import re

def check_directory_existence(directory_path):
    """
    Check if a directory exists and create it if it doesn't.

    Parameters:
    directory_path (str): The path of the directory to check.

    Returns:
    None
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")
    else:
        print(f"Directory '{directory_path}' already exists.")

def unzip_gzip_file(zipped_file_path: str, unzipped_filepath: str):
    """
    Unzips a gzip file and saves the contents to a specified file path.

    Args:
        zipped_file_path (str): The path to the gzip file to be unzipped.
        unzipped_filepath (str): The path where the unzipped file will be saved.

    Returns:
        None
    """
    with gzip.open(zipped_file_path, 'rb') as gz_file:
        with open(unzipped_filepath, 'wb') as output_file:
            output_file.write(gz_file.read())



def find_elements_between(text: str):
    """
    Find all elements between square brackets in the given text.

    Parameters:
        text (str): The input text to search for elements.

    Returns:
        list: A list of all elements found between square brackets in the text.
    """
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, text)
    return matches

def get_tair_id_from_description(description: str):
    """
    Given a description string, this function searches for elements enclosed in square brackets and 
    checks if any of the elements start with 'db_xref='. If such an element is found, it splits the 
    element by '=' and then by ',' to get a list of cross references. It then checks if any of the 
    cross references start with 'TAIR:' and if so, it returns the ID after the ':' character. 

    Args:
        description (str): The input string from which to extract the TAIR ID.

    Returns:
        str or None: The TAIR ID if found, or None if no TAIR ID is found.
    """
    descriptors = find_elements_between(description)
    for i in descriptors:
        if i.startswith('db_xref='):
            cross_references = i.split('=')[-1].split(',')
            for j in cross_references:
                if j.startswith('TAIR:'):
                    return j.split(':')[-1]
