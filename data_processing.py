import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def load_data(filepath):
    """
    
    """
    df = pd.read_csv(filepath)

    eye_loc = df[df["Point"] == "Eye"][["X (in)", "Y (in)"]].to_numpy()

    # extract points and make eye as origin
    car_points = df[df["Point"].str.contains("Car")][["X (in)", "Y (in)"]].to_numpy() - eye_loc
    nvp_points = df[df["Point"].str.contains("Car|Eye") == False][["X (in)", "Y (in)"]].to_numpy() - eye_loc
    eye_loc -= eye_loc

    # flip y-coordinate to reflect across x-axis
    car_points[:, 1] = car_points[:, 1] * -1
    nvp_points[:, 1] = nvp_points[:, 1] * -1
    eye_loc[:, 1] = eye_loc[:, 1] * -1
    
    # add two more columns of each set of points in polar
    car_points = np.concatenate((car_points, cart_to_polar(car_points)), axis=1)
    nvp_points = np.concatenate((nvp_points, cart_to_polar(nvp_points)), axis=1)
    eye_loc = np.concatenate((eye_loc, cart_to_polar(eye_loc)), axis=1)

    # sort each matrix by theta (last col of points matrix)
    car_points = car_points[car_points[:, 3].argsort()[::-1]]
    nvp_points = nvp_points[nvp_points[:, 3].argsort()[::-1]]
    eye_loc = eye_loc[eye_loc[:, 3].argsort()[::-1]]

    return eye_loc, car_points, nvp_points

def cart_to_polar(pts):
    """
    
    """
    x = pts[:, 0]
    y = pts[:, 1]

    r = np.sqrt(np.square(x) + np.square(y)).reshape((np.shape(pts)[0], -1))
    theta = np.arctan2(y, x).reshape((np.shape(pts)[0], -1)) # radians

    return np.concatenate((r, theta), axis=1)

def plot_data(eye_pt, car_pts, nvp_pts):
    """
    
    """
    # extract coordinates
    car_x = car_pts[:, 0] 
    car_y = car_pts[:, 1]
    nvp_x = nvp_pts[:, 0]
    nvp_y = nvp_pts[:, 1]
    eye_x = eye_pt[:, 0]
    eye_y = eye_pt[:, 1]

    car_r = car_pts[:, 2] 
    car_theta = car_pts[:, 3]
    nvp_r = nvp_pts[:, 2]
    nvp_theta = nvp_pts[:, 3]
    eye_r = eye_pt[:, 2]
    eye_theta = eye_pt[:, 3]

    fig1 = plt.figure()
    ax_pol = fig1.add_subplot(projection="polar")
    ax_pol.scatter(nvp_theta, nvp_r, c="#00ff00")
    ax_pol.scatter(car_theta, car_r, c="#ff0000")
    ax_pol.scatter(eye_theta, eye_r, c="#0000ff")

    fig2 = plt.figure()
    ax_cart = fig2.add_subplot()
    ax_cart.scatter(nvp_x, nvp_y, c="#00ff00")
    ax_cart.scatter(car_x, car_y, c="#ff0000")
    ax_cart.scatter(eye_x, eye_y, c="#0000ff")
    
    plt.show()
    


