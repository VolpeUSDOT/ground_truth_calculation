"""
Old Code - Load and process ground truth data for a single vehicle that contains
car points, nvp points, and eye points.
"""
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def load_data(filepath):
    """
    Given a filepath to a ground truth csv file extract the car, nvp, and eye
    points and process them.

    Args:
        filepath: a path to a csv file
    Returns:
        eye_loc: a numpy array containing the x and y coordinates of the eye point
            and the r and theta coordinates of the eye point
        car_points: a numpy array containing the x and y coordinates of the car points
            and the r and theta coordinates of the car points
        nvp_points: a numpy array containing the x and y coordinates of the nvp points
            and the r and theta coordinates of the nvp points
    """
    df = pd.read_csv(filepath)

    eye_loc = df[df["Point"] == "Eye"][["x (in)", "y (in)"]].to_numpy()

    # extract points and make eye as origin
    car_points = (
        df[df["Point"].str.contains("Car")][["x (in)", "y (in)"]].to_numpy() - eye_loc
    )
    nvp_points = (
        df[df["Point"].str.contains("Car|Eye") == False][
            ["x (in)", "y (in)"]
        ].to_numpy()
        - eye_loc
    )
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
    Adjust car points to start and stop at the same angle as the nvp points.

    Args:
        car_points: a numpy array containing the x and y coordinates of the car points
            and the r and theta coordinates of the car points
        nvp_points: a numpy array containing the x and y coordinates of the nvp points
            and the r and theta coordinates of the nvp points
    Returns:
        car_points_trimmed: a numpy array containing the x and y coordinates of the car
            points and the r and theta coordinates of the car points after fixing
            bounds
    """
    car_points_trimmed = trim_car_data(car_points, nvp_points)

    left_bound = get_intersection(car_points_trimmed[0:2, :], nvp_points[0, :])
    right_bound = get_intersection(car_points_trimmed[-2:, :], nvp_points[-1, :])

    car_points_trimmed[0, :] = left_bound
    car_points_trimmed[-1, :] = right_bound

    return car_points_trimmed


def trim_car_data(car_points, nvp_points):
    """
    Trim car points to start just before the first nvp point and stop just after the
    last nvp point.

    Args:
        car_points: a numpy array containing the x and y coordinates of the car points
            and the r and theta coordinates of the car points
        nvp_points: a numpy array containing the x and y coordinates of the nvp points
            and the r and theta coordinates of the nvp points
    Returns:
        car_points_trimmed: a numpy array containing the x and y coordinates of the car
            points and the r and theta coordinates of the car points after trimming
    """
    num_car_points = np.shape(car_points)[0]

    leftmost_ang = nvp_points[0, 3]
    rightmost_ang = nvp_points[-1, 3]

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
    Given an NVP and two points on the car the bound it (one point on the left and
    one point on the right) find the point of intersection between the line formed
    by the two car points and the line formed by the NVP and the origin.

    Args:
        car_pair: a numpy array containing the x and y coordinates of the car points
            and the r and theta coordinates of the car points
        nvp_point: a numpy array containing the x and y coordinates of the nvp point
            and the r and theta coordinates of the nvp point
    Returns:
        ordered_pair: a numpy array containing the x and y coordinates of the point
            of intersection and the r and theta coordinates of the point of intersection
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
    Convert a set of points from cartesian coordinates to polar coordinates.

    Args:
        pts: a numpy array containing the x and y coordinates of the points
    Returns:
        res: a numpy array containing the r and theta coordinates of the points
    """
    x = pts[:, 0]
    y = pts[:, 1]

    r = np.sqrt(np.square(x) + np.square(y)).reshape((np.shape(pts)[0], -1))

    # angles in quad 1 and 2 are pos, angles in quad 3 and 4 are neg
    theta = np.arctan2(y, x).reshape((np.shape(pts)[0], -1))  # radians

    # make values in the third quadrant positive so that sorting points wraps
    # from back of car clockwise after sorting points by angle
    theta += np.ones((np.shape(theta)[0], 1)) * 2 * np.pi * (theta < -np.pi / 2)

    return np.concatenate((r, theta), axis=1)


def plot_data(eye_pt, car_pts, nvp_pts):
    """
    Plot eye point, car points, and nvp points on a polar plot and a cartesian plot
    in different colors.

    Args:
        eye_pt: a numpy array containing the x and y coordinates of the eye point
            and the r and theta coordinates of the eye point
        car_pts: a numpy array containing the x and y coordinates of the car points
            and the r and theta coordinates of the car points
        nvp_pts: a numpy array containing the x and y coordinates of the nvp points
            and the r and theta coordinates of the nvp points
    Returns:
        N/A
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

    fig1 = plt.figure(figsize=(10, 5))
    ax_pol = fig1.add_subplot(121, projection="polar")
    ax_pol.scatter(nvp_theta, nvp_r, c="#00ff00")
    ax_pol.scatter(car_theta, car_r, c="#ff0000")
    ax_pol.scatter(eye_theta, eye_r, c="#0000ff")

    ax_cart = fig1.add_subplot(122)
    ax_cart.scatter(nvp_x, nvp_y, c="#00ff00")
    ax_cart.scatter(car_x, car_y, c="#ff0000")
    ax_cart.scatter(eye_x, eye_y, c="#0000ff")
    ax_cart.set_aspect("equal", "box")

    plt.show()
