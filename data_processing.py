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

def fix_car_bounds(car_points, nvp_points):
    """
    
    """
    car_points_trimmed = trim_car_data(car_points, nvp_points)

    left_bound = get_intersection(car_points_trimmed[0:2, :], nvp_points[0, :])
    right_bound = get_intersection(car_points_trimmed[-2:, :], nvp_points[-1, :])
    
    car_points_trimmed[0, :] = left_bound
    car_points_trimmed[-1, :] = right_bound

    return car_points_trimmed

def trim_car_data(car_points, nvp_points):
    """
    
    """
    num_car_points = np.shape(car_points)[0]

    leftmost_ang = nvp_points[0, 3]
    rightmost_ang = nvp_points[-1, 3]
    print(leftmost_ang, rightmost_ang)

    left_bound_index = None
    right_bound_index = None
    for i in range(num_car_points):
        if car_points[i, 3] < leftmost_ang and left_bound_index is None:
            left_bound_index = i
        if car_points[i, 3] < rightmost_ang and right_bound_index is None:
            right_bound_index = i
    
    car_points_trimmed = car_points[left_bound_index - 1 : right_bound_index + 1, :]

    return car_points_trimmed

def get_intersection(car_pair, nvp_point):
    """
    
    """
    car_point1 = car_pair[0]
    car_point2 = car_pair[1]

    car_slope = (car_point2[1] - car_point1[1]) / (car_point2[0] - car_point1[0])
    nvp_slope = nvp_point[1] / nvp_point[0]

    x_int = ((car_slope * car_point1[0]) - car_point1[1]) / (car_slope - nvp_slope)
    y_int = nvp_slope * x_int

    ordered_pair = np.array([[x_int, y_int]])

    return np.concatenate((ordered_pair, cart_to_polar(ordered_pair)), axis=1)

def cart_to_polar(pts):
    """
    
    """
    x = pts[:, 0]
    y = pts[:, 1]

    r = np.sqrt(np.square(x) + np.square(y)).reshape((np.shape(pts)[0], -1))
    
    # angles in quad 1 and 2 are pos, angles in quad 3 and 4 are neg
    theta = np.arctan2(y, x).reshape((np.shape(pts)[0], -1)) # radians

    # make values in the third quadrant positive so that sorting points wraps
    # from back of car clockwise after sorting points by angle 
    theta += np.ones((np.shape(theta)[0], 1)) * 2 * np.pi * (theta < -np.pi / 2)

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
    


