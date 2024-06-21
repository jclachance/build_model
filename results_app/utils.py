import cobra
import pandas as pd

def get_model(path):
    if not path.endswith('.json'):
        raise ValueError('Please provide a path to a model in JSON format')
    else:
        model = cobra.io.load_json_model(path)
    return model