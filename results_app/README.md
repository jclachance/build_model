# Results app

Welcome to the results app. This streamlit app allows you to select different modleing options and return the results live.

## Usage

1. Ensure you copied the functional model (in json format) generated in the build_model.ipynb notebook under a results_app/models folder.
2. Build and run the docker image. A dockerfile and requirements are provided that enable you to run the app on any platform. Make sure you have docker installed on your machine: https://docs.docker.com/engine/install/. Follow these instructions:
    2.1 Build the Docker image:
    ```
    cd results_app
    docker build -t build_model_app .
    ```
    2.2 Run the Docker container:
    ```
    docker run -p 8501:8501 build_model_app
    ```
    This will create a Docker image for the Streamlit app and run it on port 8501. Follow this link to display the app in your browser.

3. From the app, your modeling parameters are in the sidebar. Select the model from the list of models present in your results_app/models folder. Then select your target metabolite (Cellulose or Pectin). Finally, select the number of samples to run, the highger the number, the longer it will take to generate but the more quality results you will obtain. 
4. Submit your modeling options. The app will load the model and execute flux sampling. After about 2 minutes, your most distinct flux distributions will be shown. 