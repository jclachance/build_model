
import os
from unittest.mock import patch
import pytest
from utils.genome_mapping import build_diamond_database, run_diamond

class TestGenomeMapping:
    def test_build_diamond_database_valid_input(self, tmpdir):
        # Create a temporary directory for the test
        outdir = tmpdir.mkdir("test_out")

        # Create a test input file
        inputfile = tmpdir.join("test_data.fasta")
        inputfile.write(">seq1\nACGT\n>seq2\nACGTACGT\n")

        # Call the function with the test input file and output directory
        build_diamond_database(str(inputfile), str(outdir))

        # Check that the diamond database was successfully built
        assert os.path.isfile(os.path.join(str(outdir), f"{inputfile}.dmnd"))

    def test_build_diamond_database_nonexistent_input(self, tmpdir):
        # Create a temporary directory for the test
        outdir = tmpdir.mkdir("test_out")

        # Call the function with a nonexistent input file
        inputfile = "nonexistent_file.fasta"
        with pytest.raises(ValueError):
            build_diamond_database(inputfile, str(outdir))

    def test_build_diamond_database_failure(self, tmpdir):
        # Create a temporary directory for the test
        outdir = tmpdir.mkdir("test_out")

        # Create a test input file
        inputfile = tmpdir.join("test_data.fasta")
        inputfile.write(">seq1\nACGT\n>seq2\nACGTACGT\n")

        # Mock the subprocess call to raise an exception
        with patch('subprocess.call', side_effect=Exception("Mocked exception")):
            with pytest.raises(RuntimeError):
                build_diamond_database(str(inputfile), str(outdir))

    def test_run_diamond_protein_valid_input(self, tmpdir):
        # Create a temporary directory for the test
        diamond_path = tmpdir.mkdir("diamond")
        genome_path = tmpdir.mkdir("genome")

        # Create a test input file and database
        inputfile = genome_path.join("test_protein.fasta")
        inputfile.write(">seq1\nACGT\n>seq2\nACGTACGT\n")
        database = diamond_path.join("test_database.dmnd")

        # Call the function with the test input file and database
        run_diamond(str(inputfile), str(database))

        # Check that the output file was created
        assert os.path.isfile(os.path.join(str(diamond_path), f"test_protein.fasta_vs_test_database.dmnd.tsv"))

    def test_run_diamond_invalid_input_type(self, tmpdir):
        # Create a temporary directory for the test
        diamond_path = tmpdir.mkdir("diamond")
        genome_path = tmpdir.mkdir("genome")

        # Create a test input file and database
        inputfile = genome_path.join("test_protein.fasta")
        inputfile.write(">seq1\nACGT\n>seq2\nACGTACGT\n")
        database = diamond_path.join("test_database.dmnd")

        # Call the function with an invalid input type
        with pytest.raises(AssertionError):
            run_diamond(str(inputfile), str(database), input_type='invalid')

    def test_run_diamond_failure(self, tmpdir):
        # Create a temporary directory for the test
        diamond_path = tmpdir.mkdir("diamond")
        genome_path = tmpdir.mkdir("genome")

        # Create a test input file and database
        inputfile = genome_path.join("test_protein.fasta")
        inputfile.write(">seq1\nACGT\n>seq2\nACGTACGT\n")
        database = diamond_path.join("test_database.dmnd")

        # Mock the subprocess call to raise an exception
        with patch('subprocess.call', side_effect=Exception("Mocked exception")):
            with pytest.raises(RuntimeError):
                run_diamond(str(inputfile), str(database))