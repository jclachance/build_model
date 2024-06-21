import pandas as pd
from utils.utilities import get_tair_id_from_description
from utils.data_io import load_arabidopsis_model
from Bio import SeqIO

import cobra
from cobra.manipulation.delete import remove_genes
from cobra.flux_analysis import single_gene_deletion, double_gene_deletion

def get_model_gene_to_proteome_map(arabidopsis_proteome: str, diamond_mapping: pd.DataFrame) -> dict:
    """
    Get a mapping of Arabidopsis thaliana model genes to protein identifiers from the proteome.

    Args:
        arabidopsis_proteome (str): The path to the Arabidopsis thaliana proteome file in FASTA format.
        diamond_mapping (pd.DataFrame): The diamond mapping dataframe obtained from parse_diamond_output()

    Returns:
        dict: A dictionary mapping Arabidopsis thaliana model genes to protein identifiers.
            The keys are the model gene IDs and the values are the corresponding protein identifiers.
    """
    # Map the Arabidopsis thaliana model genes to protein identifiers from the proteome
    records = SeqIO.parse(arabidopsis_proteome, 'fasta')
    genome_to_model_mapping = {i.id: get_tair_id_from_description(i.description)for i in records.records}
    # Use this mapping to add a column to the dataframe
    tair_col = [genome_to_model_mapping.get(i) for i in diamond_mapping.sseqid]
    diamond_mapping['TAIR_ID'] = tair_col
    return diamond_mapping


def get_model_genes_to_remove(diamond_mapping: pd.DataFrame, model: cobra.Model, verbose=True) -> list:
    """
    Given a DataFrame `diamond_mapping` containing protein-gene mappings and a `cobra.Model` `model` representing the Arabidopsis thaliana reference model, 
    this function returns a list of genes that should be removed from the reference model.
    
    Args:
        diamond_mapping (pd.DataFrame): A DataFrame containing protein-gene mappings. It should have a column named 'TAIR_ID' that contains the TAIR IDs of the target species genes.
        model (cobra.Model): A `cobra.Model` representing the Arabidopsis thaliana reference model.
        verbose (bool, optional): If True, prints the number of target species genes found in Arabidopsis thaliana and the number of target species found in the reference model. Defaults to True.
    
    Returns:
        list: A list of genes that should be removed from the reference model.
    """
    # The non redundant list of TAIR IDs in the diamond_mapping is a list that can be mapped to the A. thaliana model to produce a reduced version of it
    target_genes = list(set(diamond_mapping['TAIR_ID'].drop_duplicates().dropna().to_list()))
    if verbose:
        print(f"{len(target_genes)} target species genes were found in the reference proteome")
    # Now map those genes to the model
    target_model_genes = [g.id for g in model.genes if g.id in target_genes]
    if verbose:
        print(f"{len(target_model_genes)} target species were found in the reference model containing {len(model.genes)}")
    genes_to_remove = [g for g in model.genes if g.id not in target_model_genes]
    if verbose:
        print(f"{len(genes_to_remove)} genes must be removed from the reference model")
    return genes_to_remove

def get_essential_genes(model: cobra.Model) -> list:
    """
    A wrapper around the single gene deletion function from Cobra.
    Returns a list of essential genes. The elements of that list are the genes identifier as strings.

    Args:
        model (cobra.Model): The model from which the essential genes will be extracted.

    Returns:
        list: A list of essential genes.
    """
    deletion_results = single_gene_deletion(model)
    essential_genes = [list(i)[0] for i in deletion_results[deletion_results['growth'] != 10]['ids'].to_list()]
    return essential_genes

def get_exchange_genes(model):
    """
    Given a `cobra.Model` `model`, this function returns a list of gene IDs that are involved in exchange reactions.

    Parameters:
        model (cobra.Model): The model from which exchange genes will be extracted.

    Returns:
        list: A list of gene IDs that are involved in exchange reactions.
    """
    exchange_genes = []
    for r in model.exchanges:
        exchange_genes.append([g.id for g in r.genes])

    exchange_genes = list(set([i for l in exchange_genes for i in l]))
    return exchange_genes

def get_synthetic_lethals(model: cobra.Model, genes_to_remove: list) -> list:
    """
    Given a `cobra.Model` `model` and a list of `genes_to_remove`, this function returns a list of gene IDs that are synthetic lethal to the model when both `gene_list1` and `gene_list2` are set to `genes_to_remove`.

    Args:
        model (cobra.Model): The model from which synthetic lethal genes will be identified.
        genes_to_remove (list): A list of gene IDs to be removed from the model.

    Returns:
        list: A list of gene IDs that are synthetic lethal to the model when both `gene_list1` and `gene_list2` are set to `genes_to_remove`.
    """
    synthetic_lethals = double_gene_deletion(model, gene_list1=genes_to_remove, gene_list2=genes_to_remove)
    l = [i for s in synthetic_lethals[synthetic_lethals['growth']!=10]['ids'] for i in list(s)]
    return l

def prune_genes_to_remove(model: cobra.Model, genes_to_remove: list) -> list:
    """
    Prunes the list of genes to remove from a given model by excluding essential genes and genes from exchange reactions.
    
    Args:
        model (cobra.Model): The model from which genes will be pruned.
        genes_to_remove (list): A list of gene IDs to be removed from the model.
        
    Returns:
        list: A list of gene IDs that can be safely removed from the model.
    """
    # Identify the essential genes in this model
    essential_genes = get_essential_genes(model)
    # Edit the genes to remove to avoid removing essential genes that will prevent the model from solving
    genes_to_remove = set([g.id for g in genes_to_remove]) - set(essential_genes)
    # Do not remove the genes from the exchange reactions either
    exchanges_genes = get_exchange_genes(model)
    genes_to_remove = set(genes_to_remove) - set(exchanges_genes)
    synthetic_lethals = get_synthetic_lethals(model, genes_to_remove)
    genes_to_remove = set(genes_to_remove) - set(synthetic_lethals)
    return genes_to_remove

def generate_base_model(genes_to_remove: list, save_path: str, model: cobra.Model=None):
    """
    Generate a base model by removing specified genes from the given model and saving the output to the specified path.

    Args:
        genes_to_remove (list): A list of gene IDs to be removed from the model.
        save_path (str): The path where the modified model will be saved.
        model (cobra.Model, optional): The model from which genes will be removed. If not provided, a new model will be loaded using the `load_arabidopsis_model` function. Defaults to None.

    Returns:
        None
    """
    # It is safer to load a new model, modify it in place and saving the output
    if model is None:
        model = load_arabidopsis_model()

    remove_genes(model, genes_to_remove, remove_reactions=True)

    # It is safer to save the model
    cobra.io.save_json_model(model, save_path)

def gapfill_base_model(outfile: str):
    """
    Gapfills the base model by adding reactions that are not present in the base model from the loaded model.
    
    Args:
        outfile (str): The path to save the gapfilled base model.
    
    Returns:
        None
    """
    model = load_arabidopsis_model()
    base_model = cobra.io.load_json_model(os.path.join('./models','hirsutum_base_model.json'))
    print("Loaded both models, now checking reactions one at a time")
    for r in model.reactions:
        if r.id not in [react.id for react in base_model.reactions]:
            # base_model = cobra.io.load_json_model(os.path.join('./models','hirsutum_base_model.json'))
            # print(f"Loaded the model for {r.id}")
            base_model.add_reactions([r])
            solution = base_model.optimize()
            if not solution.status == 'infeasible':
                print(f"Added {r.id} and it solves the model with value {solution.objective_value}")
                cobra.io.save_json_model(base_model, outfile)
                break
