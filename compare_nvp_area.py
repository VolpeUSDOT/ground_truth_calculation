from validation_data_processing import load_data, plot_data
from ground_truth_shadow import get_area, get_distance
import numpy as np

def main():
    datasets = load_data()
    labels = ["Markerless", "VIEW 1.0", "Ground Truth", "Markerless Rig", "VIEW 1.0 Rig", "Ground Truth Rig"]

    eye_point = np.array([[0, 0]])
    nvp_areas = []

    for dataset in datasets:
        num_nvp_points = np.shape(dataset)[0]
        nvp_area = 0
        for i in range(num_nvp_points - 1):
            # print(dataset[i])
            left_dist = get_distance(eye_point[0], dataset[i])
            right_dist = get_distance(eye_point[0], dataset[i+1])
            between_dist = get_distance(dataset[i], dataset[i+1])

            triangle_area = get_area(left_dist, right_dist, between_dist)

            nvp_area += triangle_area
        nvp_areas.append(nvp_area)
    
    for i, label in enumerate(labels):
        print(f"NVP Area for {label}: {nvp_areas[i]} sq. ft. Percent Error: {((nvp_areas[i] - nvp_areas[-1]) / nvp_areas[-1]) * 100: .2f}%")

    # w/o rig
    plot_data(datasets[:-3], labels[:-3])
    # plot just rig
    plot_data(datasets[-3:], labels[-3:])

if __name__=="__main__":
    main()