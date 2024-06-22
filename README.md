# build_model
This repository contains a workflow for reconstructing a metabolic model for Gossypium hirsutum (Cotton) using homology search of functions to the Arabidopsis thaliana model. The workflow also includes a Streamlit app for making predictions and performing analysis on the reconstructed model.

# Workflow Overview
The workflow consists of two main components:

1. **Template Model Reconstruction**: This component utilizes homology search to identify functions relevant to the metabolism of Gossypium hirsutum by comparing the Arabidopsis thaliana model to the Gossypium hirsutum genome. The identified functions are then used to reconstruct a template model for Gossypium hirsutum.
2. **Model Predictions and Analysis**: This component provides a Streamlit app that allows users to make predictions and perform analysis on the reconstructed model. The app includes functionalities for simulating metabolic fluxes, visualizing metabolic pathways, and exploring the metabolic network.


# Getting Started
To get started with the workflow, follow these steps:

1. Clone the repository: 
```
git clone https://github.com/jclachance/build_model.git
```
2. Create a Python virtual environment of your choice and install the required dependencies: 
```
pip install -r requirements.txt
```
3. Create a *G. hirsutum* model using the ```build_model.ipynb``` notebook.

4. Perform live model simulation analysis using the streamlit ```results_app```

# Streamlit app local deployment with Docker
You can deploy the Streamlit app using Docker by following these steps:

1. Build the Docker image:
```
docker build -t build_model_app .
```
2. Run the Docker container:
```
docker run -p 8501:8501 build_model_app
```

This will create a Docker image for the Streamlit app and run it on port 8501. Follow this link to display the app in your browser.

**Before you run the app**: copy your models into the models folder in the results_app. 

# Testing
To run the tests, follow these steps:

1. Change to the tests directory: 
```
cd tests
```
2. Run the tests using pytest: 
```
pytest
```


The tests cover various aspects of the workflow, including template model reconstruction and model predictions and analysis.

# Contributing
Contributions to the workflow are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

# License
This workflow is licensed under the MIT License. See the LICENSE file for details.
