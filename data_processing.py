import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def load_data(filepath):
    """
    
    """
    df = pd.read_csv(filepath)

    eye_loc = df[df["Point"] == "Eye"][["X (in)", "Y (in)"]].to_numpy()[0]
    car_points = df[df["Point"].str.contains("Car")][["X (in)", "Y (in)"]].to_numpy()
    nvp_points = df[df["Point"].str.contains("Car|Eye") == False][["X (in)", "Y (in)"]].to_numpy()
    
    return eye_loc, car_points, nvp_points

def plot_data(eye_pt, car_pts, nvp_pts):
    """
    
    """
    car_x = car_pts[:, 0] 
    car_y = car_pts[:, 1]
    nvp_x = nvp_pts[:, 0]
    nvp_y = nvp_pts[:, 1]
    eye_x = eye_pt[0]
    eye_y = eye_pt[1]
    plt.title("NVP Measurements") 
    plt.xlabel("X Direction (in)") 
    plt.ylabel("Y Direction (in)") 
    plt.scatter(x=nvp_x, y=nvp_y, c="#00ff00")
    plt.scatter(x=car_x, y=car_y, c="#ff0000")
    plt.scatter(x=eye_x, y=eye_y, c ="#0000ff")
    plt.show()


