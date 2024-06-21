import os
from subprocess import call
import pandas as pd

def build_diamond_database(inputfile: str, genome_path: str=None, outdir: str=None):
    """
    Builds a diamond database from an input file.

    Args:
        inputfile (str): The path to the input file.
        genome_path (str, optional): The path to the genome directory. Defaults to './'.
        outdir (str, optional): The path to the output directory. Defaults to None.

    Raises:
        ValueError: If the input file does not exist.
        RuntimeError: If the diamond database build fails.

    Returns:
        None
    """
    if genome_path is None:
        genome_path = os.path.dirname(inputfile)

    reference = os.path.join(genome_path, inputfile)

    if not os.path.isfile(reference):
        raise ValueError(f"Reference genome {reference} does not exist.")
    
    if outdir is None:
        outdir = os.path.dirname(reference)

    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    database = os.path.join(outdir,f"{inputfile}.dmnd")
    
    cmd = f"diamond makedb --in {reference} -d {database}"
    try:
        call(cmd, shell=True)
    except Exception as e:
        raise RuntimeError(f"Failed to build diamond database: {e}")

def run_diamond(inputfile: str, database: str, outputfile: str=None, genome_path: str='./', diamond_path: str=None, input_type: str='protein', args: list=None):
    """
    Runs the Diamond BLASTP command-line tool to perform protein or DNA sequence alignment.

    Args:
        inputfile (str): The path to the input file containing the sequences to be aligned.
        database (str): The path to the Diamond database to search against.
        outputfile (str, optional): The path to the output file where the results will be saved. If not provided, the output file will be named as "{inputfile}_vs_{database.split('/')[-1]}.tsv".
        genome_path (str, optional): The path to the directory containing the input file. Defaults to './'.
        diamond_path (str, optional): The path to the directory containing the Diamond executable. If not provided, the current directory will be used.
        input_type (str, optional): The type of sequences in the input file. Must be either 'protein' or 'dna'. Defaults to 'protein'.
        args (str, optional): Additional arguments to be passed to the Diamond command-line tool. If not provided, the default arguments will be used.

    Raises:
        AssertionError: If the input_type is not 'protein' or 'dna'.
        RuntimeError: If the Diamond command-line tool fails to run.

    Returns:
        None
    """
    assert (input_type in ['protein', 'dna']), "Input type must be either 'protein' or 'dna'."

    if outputfile is None:
        outputfile = f"{inputfile.split('/')[-1]}_vs_{database.split('/')[-1]}.tsv"

    if diamond_path is None:
        diamond_path = os.path.dirname(inputfile)

    if not os.path.isdir(diamond_path):
        os.makedirs(diamond_path)

    if args is None:
        args = "--iterate --ultra-sensitive --max-target-seqs 1 --quiet"

    queries = os.path.join(genome_path, inputfile)
    reference = os.path.join(diamond_path, database)
    outfile = os.path.join(diamond_path, outputfile)
    cmd = f"diamond blastp -d {reference} -q {queries} -o {outfile} {args}"

    try:
        call(cmd, shell=True)
    except Exception as e:
        raise RuntimeError(f"Failed to run diamond: {e}")
    
def parse_diamond_output(diamond_path: str, outputfile: str) -> pd.DataFrame:
    """Reads the Diamond output file and returns a pandas DataFrame.

    Args:
        diamond_path (str): The path where the Diamond output file is located.
        outputfile (str): The name of the Diamond output file.

    Returns:
        pd.DataFrame: 
    """
    # Parse the Diamond output
    BLAST_HEADER = 'qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore'.split(' ')
    diamond_mapping = pd.read_csv(os.path.join(diamond_path, outputfile), sep='\t', names=BLAST_HEADER)
    return diamond_mapping
