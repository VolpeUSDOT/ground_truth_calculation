import pandas
import numpy as np

def load_data(filepath):
    """
    
    """
    data_raw = pandas.read_csv(filepath)
    print(data_raw)