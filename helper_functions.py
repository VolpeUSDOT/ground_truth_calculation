"""
File containing helper functions for the main program.
"""
import math
import numpy as np


def get_distance(point1, point2):
    """
    Calculate cartesian distance between two points

    Args:
        point1, point2: 1D numpy arrays of length 2, x and y coordinates (in default units)
    Returns:
        A float representing the distance between the points (in default units)
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_area(side1, side2, side3):
    """
    Calculate the area of a triangle using Heron's forumla

    Args:
        side1, side2, side3: Floats representing the side lengths of a triangle (in defualt units)
    Returns:
        A float representing the area of the triangle (in square default units)
    """
    semiperimeter = (side1 + side2 + side3) / 2
    return math.sqrt(
        (semiperimeter)
        * (semiperimeter - side1)
        * (semiperimeter - side2)
        * (semiperimeter - side3)
    )


def cart_to_polar(pts):
    """
    Convert cartesian coordinates to polar coordinates

    Args:
        pts: a numpy array of shape (n, 2) containing the x and y coordinates of n points
    Returns:
        A numpy array of shape (n, 2) containing the r and theta coordinates of n points
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


def get_intersection(point_pair, third_point):
    """
    Given a pair of points and a third point, calculate the intersection between
    a line drawn between the pair of points and the line drawn through the third
    point and the origin.

    Args:
        point_pair: a numpy array of shape (2, 2) containing the x and y coordinates of two points
        third_point: a numpy array of shape (1, 2) containing the x and y coordinates of a point
    Returns:
        A numpy array of shape (1, 4) containing the x and y coordinates of the intersection
        point and the r and theta coordinates of the intersection point
    """
    point1 = point_pair[0]
    point2 = point_pair[1]

    point_slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
    third_point_slope = third_point[1] / third_point[0]

    x_int = ((point_slope * point1[0]) - point1[1]) / (point_slope - third_point_slope)
    y_int = third_point_slope * x_int

    ordered_pair = np.array([[x_int, y_int]])

    return np.concatenate((ordered_pair, cart_to_polar(ordered_pair)), axis=1)
