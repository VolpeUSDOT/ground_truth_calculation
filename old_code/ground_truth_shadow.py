"""
Old Code - Main function to calculate the shadow area of a vehicle given its
nvp points, car points, and eye point.
"""
import numpy as np
import math

from data_processing import load_data, fix_car_bounds, plot_data


def main():
    # file to read from
    testfile = "../Data/TestData.csv"
    hondafile = "../Data/HondaOdysseyGroundTruth.csv"

    # load and format data
    eye_point, car_points, nvp_points = load_data(hondafile)
    processed_car_points = fix_car_bounds(car_points, nvp_points)

    # calculate nvp area
    num_nvp_points = np.shape(nvp_points)[0]
    nvp_area = 0
    for i in range(num_nvp_points - 1):
        left_dist = get_distance(eye_point[0], nvp_points[i])
        right_dist = get_distance(eye_point[0], nvp_points[i + 1])
        between_dist = get_distance(nvp_points[i], nvp_points[i + 1])

        triangle_area = get_area(left_dist, right_dist, between_dist)

        nvp_area += triangle_area
    print(nvp_area)  # square inches

    # calculate car area
    num_processed_car_points = np.shape(processed_car_points)[0]
    car_area = 0
    for i in range(num_processed_car_points - 1):
        left_dist = get_distance(eye_point[0], processed_car_points[i])
        right_dist = get_distance(eye_point[0], processed_car_points[i + 1])
        between_dist = get_distance(
            processed_car_points[i], processed_car_points[i + 1]
        )

        triangle_area = get_area(left_dist, right_dist, between_dist)

        car_area += triangle_area
    print(car_area)  # square inches

    # calculate shadow area
    shadow_area = nvp_area - car_area

    print(f"Shadow Area: {shadow_area} sq. in.")

    # plot data
    plot_data(eye_point, processed_car_points, nvp_points)


def get_distance(point1, point2):
    """
    Calculate cartesian distance between two points

    Args:
        point1, point2: 1D numpy arrays of length 2, x and y coordinates (in inches)
    Returns:
        A float representing the distance between the points (in inches)
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def get_area(side1, side2, side3):
    """
    Calculate the area of a triangle using Heron's forumla

    Args:
        side1, side2, side3: Floats representing the side lengths of a triangle (in default units)
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


if __name__ == "__main__":
    main()
