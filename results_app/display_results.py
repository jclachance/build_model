import pandas as pd
from utils import *
import streamlit as st
import os

st.title('Display metabolic modeling results')

st.markdown("To start using this app, select a model from the sidebar. The scrolldown will show you the models stored under results_app/models, make sure it is not empty!")

MODEL_PATH = './models'

with st.sidebar.form(key='sidebar_selection_form'):
    st.markdown('## Select your modeling options here')
    model_file = st.selectbox(
        'Select a model',
        os.listdir(MODEL_PATH)
        )
    st.markdown('## Select your target metabolite here')
    target_metabolite = st.selectbox(
        'Select a target metabolite',
        ('S_Cellulose_c', 'S_Pectin_c')
    )
    st.markdown('## Select the number of samples here')
    number_of_samples = st.number_input(
        'Number of samples',
        min_value = 50,
        max_value = 10000
    )
    modeling_options_submitted = st.form_submit_button(label = 'Submit modeling options')

if modeling_options_submitted:
    # 1. Load model
    model_load_state = st.text('Loading metabolic model...')
    model = get_model(os.path.join(MODEL_PATH, model_file))
    model_load_state.text('Loading metabolic model... Done!')    
    # 2. Perform flux sampling
    flux_sampling_state = st.text('Performing flux sampling...')
    old_objective = 'Ex16'
    new_objective = 'BIO_L'
    model = change_model_objective(old_objective, new_objective, model)
    # 2.1 Generate biomass flux samples
    biomass_samples = run_flux_sampling(model, n_samples=number_of_samples)
    flux_sampling_state.text('Performing flux sampling... Biomass flux sampling is done!')
    # 2.2 Generate target flux samples
    model, new_objective = create_exchange_reaction(model, target_metabolite)
    model = change_model_objective(old_objective, new_objective, model)
    target_samples = run_flux_sampling(model, n_samples=50)
    flux_sampling_state.text('Performing flux sampling... Target flux sampling is done!')
    # 3. Perform Kolmogorov-Smirnov test to get distribution of flux samples
    ks_test = perform_ks_test(model, biomass_samples, target_samples)
    flux_sampling_state.text('Performing flux sampling... Kolmogorov-Smirnov test is done!')
    # 4. Display results
    top_hits = get_top_hits(ks_test, n_hits=9)
    st.dataframe(top_hits)
    # 5. Plot distribution
    plot_distribution(top_hits['Reaction'].to_list(), biomass_samples, target_samples)
