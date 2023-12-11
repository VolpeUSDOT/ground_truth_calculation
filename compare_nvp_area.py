"""
Main file for comparing the NVP area of the different datasets.
"""
import numpy as np
from data_processing import load_data, plot_data
from helper_functions import get_area, get_distance


def main():
    """
    Load a set of NVP datasets, calculate the shadow area of each set of points,
    and plot the datasets on one graph.

    Args:
        N/A
    Returns:
        N/A
    """
    datasets = load_data()

    # modify these labels to match the datasets that are returned from load_data()
    labels = ["Markerless Rig", "VIEW 1.0 Rig", "Lidar Rig", "Ground Truth Rig"]

    eye_point = np.array([[0, 0]])
    nvp_areas = []

    # iterate through each dataset
    for dataset in datasets:
        num_nvp_points = np.shape(dataset)[0]
        nvp_area = 0
        # iterate through each point in the dataset
        for i in range(num_nvp_points - 1):
            # determine the side lengths of triangle formed by the eye point and two adjactent NVPs
            left_dist = get_distance(eye_point[0], dataset[i])
            right_dist = get_distance(eye_point[0], dataset[i + 1])
            between_dist = get_distance(dataset[i], dataset[i + 1])

            # use heron's formula to calculate the area of the triangle
            triangle_area = get_area(left_dist, right_dist, between_dist)

            # update the total area
            nvp_area += triangle_area
        nvp_areas.append(nvp_area)

    # determine if there is a ground truth dataset
    ground_truth_is_present = False
    for label in labels:
        if "Ground Truth" in label:
            ground_truth_is_present = True
            break

    # print the shadow area of each dataset and the percent error from the ground truth
    for i, label in enumerate(labels):
        if ground_truth_is_present and "Ground Truth" not in label:
            print(
                f"NVP Area for {label}: {nvp_areas[i]} sq. ft. Percent Error: {((nvp_areas[i] - nvp_areas[-1]) / nvp_areas[-1]) * 100: .2f}%"
            )
        else:
            print(f"NVP Area for {label}: {nvp_areas[i]} sq. ft.")

    # plot the datasets
    plot_data(datasets, labels)


if __name__ == "__main__":
    main()
