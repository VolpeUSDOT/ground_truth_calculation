"""
File containing helper functions for the main program.
"""
import math


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
