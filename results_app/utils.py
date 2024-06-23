import cobra
from cobra.flux_analysis import production_envelope
from cobra.util import linear_reaction_coefficients
from cobra.sampling import sample

import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import streamlit as st

def get_model(path: str) -> cobra.Model:
    """
    Load a COBRA model from a JSON file.

    Args:
        path (str): The path to the JSON file containing the model.

    Returns:
        cobra.Model: The loaded COBRA model.

    Raises:
        ValueError: If the provided path does not end with '.json'.
    """
    if not path.endswith('.json'):
        raise ValueError('Please provide a path to a model in JSON format')
    else:
        model = cobra.io.load_json_model(path)
    return model

def change_model_objective(initial_reaction_id: str, new_reaction_id: str, model: cobra.Model) -> cobra.Model:
    """
    Change the objective of a COBRA model by setting the objective coefficient of the initial reaction to 0 and the objective coefficient of the new reaction to 1.

    Args:
        initial_reaction_id (str): The ID of the initial reaction.
        new_reaction_id (str): The ID of the new reaction.
        model (cobra.Model): The COBRA model.

    Returns:
        cobra.Model: The modified COBRA model with the changed objective.
    """
    model.reactions.get_by_id(initial_reaction_id).objective_coefficient = 0
    model.reactions.get_by_id(new_reaction_id).objective_coefficient = 1
    return model

def create_exchange_reaction(model: cobra.Model, metabolite_id: str) -> tuple[cobra.Model, str]:
    """
    Create an exchange reaction in the given COBRA model for the specified metabolite.

    Args:
        model (cobra.Model): The COBRA model in which to create the exchange reaction.
        metabolite_id (str): The ID of the metabolite for which to create the exchange reaction.

    Returns:
        tuple[cobra.Model, str]: A tuple containing the modified COBRA model with the exchange reaction added and the ID of the new exchange reaction.
    """
    model.add_boundary(model.metabolites.get_by_id(metabolite_id), type="exchange")
    new_exchange_reaction_id = f"EX_{metabolite_id}"
    return model, new_exchange_reaction_id

def run_flux_sampling(model: cobra.Model, n_samples: int=100) -> pd.DataFrame:
    """
    Perform flux sampling on the given COBRA model.

    Args:
        model (cobra.Model): The COBRA model to sample fluxes from.
        n_samples (int, optional): The number of samples to generate. Defaults to 100.

    Returns:
        pd.DataFrame: A DataFrame containing the sampled fluxes.
    """
    s = sample(model, n_samples)
    return s

def perform_ks_test(model: cobra.Model, samples_1: pd.DataFrame, samples_2: pd.DataFrame) -> pd.DataFrame:
    """
    Perform a Kolmogorov-Smirnov test to compare the flux distributions per reaction between two dataframes.

    Args:
        model (cobra.Model): The COBRA model containing the reactions.
        samples_1 (pd.DataFrame): The first dataframe containing the flux samples for each reaction.
        samples_2 (pd.DataFrame): The second dataframe containing the flux samples for each reaction.

    Returns:
        pd.DataFrame: A dataframe containing the reaction ID, the Kolmogorov-Smirnov statistic, and the p-value for each reaction.
    """
    # Pre-filter the samples
    samples_1 = samples_1.loc[:, (samples_1 > 1e-3).any(axis=0)]
    samples_2 = samples_2.loc[:, (samples_2 > 1e-3).any(axis=0)]
    # Compare the flux distributions per reaction
    ks_data = []
    for r in model.reactions:
        if r.id in samples_1.columns and r.id in samples_2.columns:
            kstest_result = sp.stats.ks_2samp(samples_1[r.id], samples_2[r.id])
            ks_data.append([r.id, kstest_result.statistic, kstest_result.pvalue])
        else:
            pass

    ks_df = pd.DataFrame(ks_data, columns=['Reaction', 'Statistic', 'P-value'])
    return ks_df

def get_top_hits(ks_df: pd.DataFrame, n_hits: int=10) -> pd.DataFrame:
    """
    Returns the top `n_hits` rows from the DataFrame `ks_df` sorted by the 'P-value' column in descending order.

    Parameters:
        ks_df (pd.DataFrame): The DataFrame containing the reaction ID, Kolmogorov-Smirnov statistic, and p-value for each reaction.
        n_hits (int, optional): The number of top hits to return. Defaults to 10.

    Returns:
        pd.DataFrame: A DataFrame containing the top `n_hits` rows from `ks_df` sorted by the 'P-value' column in descending order.
    """
    return ks_df.sort_values(by='P-value', ascending=False).head(n_hits)

def plot_distribution(selected_reactions: list, samples_1, samples_2) -> None:
    """
    Plot the distribution of samples for the top 10 reactions with the lowest p-values.

    Args:
        ks_df (pd.DataFrame): A DataFrame containing the reaction ID, Kolmogorov-Smirnov statistic, and p-value for each reaction.
        samples_1 (pd.DataFrame): The first dataframe containing the flux samples for each reaction.
        samples_2 (pd.DataFrame): The second dataframe containing the flux samples for each reaction.

    Returns:
        None: This function does not return anything, it only plots the distribution of samples for the top 10 reactions with the lowest p-values.
    """
    ncols=3
    nrows=len(selected_reactions)//ncols
    fig, axs = plt.subplots(nrows, ncols, figsize=(10, 10))
    
    for r, ax in zip(selected_reactions, axs.flat):
        ax.hist(samples_1[r], bins=20, alpha=0.5, label='Biomass')
        ax.hist(samples_2[r], bins=20, alpha=0.5, label='Cellulose')
        ax.set_title(r)
        ax.legend()

    plt.tight_layout()
    st.pyplot(fig)
