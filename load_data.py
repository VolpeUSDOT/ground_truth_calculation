import pandas as pd

def load_data(filepath):
    """
    
    """
    df = pd.read_csv(filepath)

    eye_loc = df[df["Point"] == "Eye"][["X (in)", "Y (in)"]].to_numpy()
    car_points = df[df["Point"].str.contains("Car")][["X (in)", "Y (in)"]].to_numpy()
    nvp_points = df[df["Point"].str.contains("Car|Eye") == False][["X (in)", "Y (in)"]].to_numpy()
    
    return eye_loc, car_points, nvp_points


