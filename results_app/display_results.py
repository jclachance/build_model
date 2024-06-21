import pandas as pd
from utils import *
import streamlit as st
import os

st.title('Display metabolic modeling results')

st.markdown("To start using this app, select a model from the sidebar. The scrolldown will show you the models stored under results_app/models, make sure it is not empty!")

st.sidebar.markdown('## Select your modeling options here')

MODEL_PATH = './models'

model_file = st.sidebar.selectbox(
    'Select a model',
    os.listdir(MODEL_PATH)
)

model_load_state = st.text('Loading metabolic model...')
model = get_model(os.path.join(MODEL_PATH, model_file))
model_load_state.text('Loading metabolic model... Done!')

