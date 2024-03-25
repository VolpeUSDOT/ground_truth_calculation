"""
File containing functions to load and process the NVP data from csv files.
"""
import pandas as pd
import matplotlib.pylab as plt
import numpy as np

from helper_functions import cart_to_polar, get_intersection


def load_data():
    """
    Helper function to load data from csv files and process them into numpy arrays.
    If the data is not centered at the eye point, it will be shifted to be centered
    at the eye point.

    Args:
        N/A
    Returns:
        datasets: a list of numpy arrays containing the x and y coordinates of the NVPs
            which have been trimmed to start and stop at the same angles
    """
    # # load and process markerless - with rig
    # markerlessrig_data_raw = pd.read_csv("./Data/HondaOdysseyMarkerlessRig.csv")
    # # filter point that are too far and translate to be centered at the eye point
    # markerlessrig_nvp = markerlessrig_data_raw[
    #     (abs(markerlessrig_data_raw["x (ft)"]) <= 40)
    #     & (abs(markerlessrig_data_raw["y (ft)"]) <= 20)
    # ][["x (ft)", "y (ft)"]].to_numpy() - np.array([[1.8542, -7.5208]])
    # # filter points that are in small a-pillar window
    # markerlessrig_nvp = markerlessrig_nvp[
    #     ~(
    #         (markerlessrig_nvp[:, 0] > 13.5)
    #         & (markerlessrig_nvp[:, 0] < 15.7)
    #         & (markerlessrig_nvp[:, 1] > 9.5)
    #         & (markerlessrig_nvp[:, 1] < 13.4)
    #     )
    # ]
    # # append columns with polar coordinates
    # markerlessrig_nvp = np.concatenate(
    #     (markerlessrig_nvp, cart_to_polar(markerlessrig_nvp)), axis=1
    # )
    # # sort by angle - largest to smallest
    # markerlessrig_nvp = markerlessrig_nvp[markerlessrig_nvp[:, 3].argsort()[::-1]]

    # # load and process view1.0 rig nvps
    # view1rig_data_raw = pd.read_csv("./Data/HondaOdysseyVIEW1.0Rig.csv")
    # # filter points that are too far
    # view1rig_nvp = view1rig_data_raw[view1rig_data_raw["NVP (in)"] != 438][
    #     ["x (ft)", "y (ft)"]
    # ].to_numpy()
    # # append columns with polar coordinates
    # view1rig_nvp = np.concatenate((view1rig_nvp, cart_to_polar(view1rig_nvp)), axis=1)
    # # sort by angle - largest to smallest
    # view1rig_nvp = view1rig_nvp[view1rig_nvp[:, 3].argsort()[::-1]]

    # # load and process lidar nvps with rig setup
    # lidarrig_data_raw = pd.read_csv("./Data/HondaOdysseyLidarRig.csv")
    # # filter points that are too far
    # lidarrig_nvp = lidarrig_data_raw[(abs(lidarrig_data_raw["x (ft)"]) <= 40)][
    #     ["x (ft)", "y (ft)"]
    # ].to_numpy()
    # # append columns with polar coordinates
    # lidarrig_nvp = np.concatenate((lidarrig_nvp, cart_to_polar(lidarrig_nvp)), axis=1)
    # # sort by angle - largest to smallest
    # lidarrig_nvp = lidarrig_nvp[lidarrig_nvp[:, 3].argsort()[::-1]]

    # # load and process ground truth rig nvps
    # groundrig_data_raw = pd.read_csv("./Data/HondaOdysseyGroundTruthRig.csv")
    # # select eye point
    # groundrig_eye_loc = groundrig_data_raw[groundrig_data_raw["Point"] == "Eye"][
    #     ["x (ft)", "y (ft)"]
    # ].to_numpy()
    # # select car points and translate to be centered at the eye point
    # groundrig_nvp = (
    #     groundrig_data_raw[groundrig_data_raw["Point"] == "Car"][
    #         ["x (ft)", "y (ft)"]
    #     ].to_numpy()
    #     - groundrig_eye_loc
    # )
    # # flip across x-axis to match orientation of other datasets
    # groundrig_nvp[:, 1] = groundrig_nvp[:, 1] * -1
    # # append columns with polar coordinates
    # groundrig_nvp = np.concatenate(
    #     (groundrig_nvp, cart_to_polar(groundrig_nvp)), axis=1
    # )
    # # sort by angle - largest to smallest
    # groundrig_nvp = groundrig_nvp[groundrig_nvp[:, 3].argsort()[::-1]]

    
    ford_ground_data_raw = pd.read_csv("./Data/FordF450GroundTruth.csv")
    ford_ground_data_nvp = ford_ground_data_raw[["x (ft)", "y (ft)"]].to_numpy()
    ford_ground_data_nvp = np.concatenate((ford_ground_data_nvp, cart_to_polar(ford_ground_data_nvp)), axis=1)
    ford_ground_data_nvp = ford_ground_data_nvp[ford_ground_data_nvp[:, 3].argsort()[::-1]]

    ford_lidar_data_raw = pd.read_csv("./Data/FordF450Lidar.csv")
    ford_lidar_data_nvp = ford_lidar_data_raw[["x (ft)", "y (ft)"]].to_numpy()
    ford_lidar_data_nvp = np.concatenate((ford_lidar_data_nvp, cart_to_polar(ford_lidar_data_nvp)), axis=1)
    ford_lidar_data_nvp = ford_lidar_data_nvp[ford_lidar_data_nvp[:, 3].argsort()[::-1]]

    ford_markerless_data_raw = pd.read_csv("./Data/FordF450Markerless.csv")
    ford_markerless_data_nvp = ford_markerless_data_raw[(abs(ford_markerless_data_raw["x (ft)"]) <= 130)][["x (ft)", "y (ft)"]].to_numpy()
    ford_markerless_data_nvp = np.concatenate((ford_markerless_data_nvp, cart_to_polar(ford_markerless_data_nvp)), axis=1)
    ford_markerless_data_nvp = ford_markerless_data_nvp[ford_markerless_data_nvp[:, 3].argsort()[::-1]]
    
    # attenuator_ground_data_raw = pd.read_csv("./Data/AttenuatorGroundTruth.csv")
    # attenuator_ground_data_nvp = attenuator_ground_data_raw[["x (ft)", "y (ft)"]].to_numpy()
    # attenuator_ground_data_nvp = np.concatenate((attenuator_ground_data_nvp, cart_to_polar(attenuator_ground_data_nvp)), axis=1)
    # attenuator_ground_data_nvp = attenuator_ground_data_nvp[attenuator_ground_data_nvp[:, 3].argsort()[::-1]]

    # attenuator_lidar_data_raw = pd.read_csv("./Data/AttenuatorLidar.csv")
    # attenuator_lidar_data_nvp = attenuator_lidar_data_raw[((abs(attenuator_lidar_data_raw["x (ft)"]) <= 50) & (abs(attenuator_lidar_data_raw["y (ft)"]) <= 30))][["x (ft)", "y (ft)"]].to_numpy()
    # attenuator_lidar_data_nvp = np.concatenate((attenuator_lidar_data_nvp, cart_to_polar(attenuator_lidar_data_nvp)), axis=1)
    # attenuator_lidar_data_nvp = attenuator_lidar_data_nvp[attenuator_lidar_data_nvp[:, 3].argsort()[::-1]]

    # attenuator_markerless_data_raw = pd.read_csv("./Data/AttenuatorMarkerless.csv")
    # attenuator_markerless_data_nvp = attenuator_markerless_data_raw[["x (ft)", "y (ft)"]].to_numpy()
    # attenuator_markerless_data_nvp = np.concatenate((attenuator_markerless_data_nvp, cart_to_polar(attenuator_markerless_data_nvp)), axis=1)
    # attenuator_markerless_data_nvp = attenuator_markerless_data_nvp[attenuator_markerless_data_nvp[:, 3].argsort()[::-1]]


    datasets = [ford_markerless_data_nvp, ford_lidar_data_nvp, ford_ground_data_nvp]
    # datasets = [attenuator_markerless_data_nvp, attenuator_lidar_data_nvp, attenuator_ground_data_nvp]
    left_bound, right_bound = get_left_and_right_bound(datasets)

    return trim_datasets(datasets, left_bound, right_bound)


def get_left_and_right_bound(datasets):
    """
    Find the starting and stopping points for each dataset in a list of NVPs.

    Args:
        datasets: a list of numpy arrays containing the x and y coordinates of the NVPs
    Returns:
        left: a numpy array containing the x and y coordinates of the point with the
            largest starting angle for each dataset
        right: a numpy array containing the x and y coordinates of the point with the
            smallest ending angle for each dataset
    """
    leftmost_points = [dataset[0, :] for dataset in datasets]
    rightmost_points = [dataset[-1, :] for dataset in datasets]

    left = min(leftmost_points, key=lambda x: x[3])
    right = max(rightmost_points, key=lambda x: x[3])

    return left, right


def trim_datasets(datasets, left_bound, right_bound):
    """
    Trim a list of datasets to start and stop at the same angle.

    Args:
        datasets: a list of numpy arrays containing the x and y coordinates of the NVPs
        left_bound: a numpy array containing the x and y coordinates of the
            point with the smallest starting angle
        right_bound: a numpy array containing the x and y coordinates of the
            point with the largest ending angle
    Returns:
        res: a list of numpy arrays containing the x and y coordinates of the NVPs
            which have been adjusted to start and stop at the same angles
    """
    res = []

    # loop through the datasets
    for dataset in datasets:
        # for each dataset, find the index of the point that is just outside the
        # left bound and the point that is just outside the right bound

        # if the first point is not the left bound, loop through the points and
        # find the first point that is just outside the left bound
        if not np.array_equal(dataset[0, :], left_bound):
            left_ind = None
            for i, point in enumerate(dataset):
                if left_ind is None or point[3] > left_bound[3]:
                    left_ind = i
                else:
                    break
        else:
            left_ind = 0

        # if the last point is not the right bound, loop through the points and
        # find the last point that is just outside the right bound
        if not np.array_equal(dataset[-1, :], right_bound):
            right_ind = None
            for i, point in enumerate(dataset[::-1]):
                if right_ind is None or point[3] < right_bound[3]:
                    right_ind = len(dataset) - i
                else:
                    break
        else:
            right_ind = -1

        # create copy of the dataset that starts and stops just outside or equal to the bounds
        new_dataset = dataset[left_ind:right_ind, :]

        # if the first point is not the left bound, replace the first point with
        # the point at the intersection of the left bound angle and the two points
        # bounding it from the dataset
        if not np.array_equal(dataset[0, :], left_bound):
            new_dataset[0, :] = get_intersection(new_dataset[0:2, :], left_bound)

        # if the last point is not the right bound, replace the last point with
        # the point at the intersection of the right bound angle and the two points
        # bounding it from the dataset
        if not np.array_equal(dataset[-1, :], right_bound):
            new_dataset[-1, :] = get_intersection(new_dataset[-2:, :], right_bound)

        res.append(new_dataset)

    return res


def plot_data(datasets, names):
    """
    Create a scatterplot of overlaid NVPs.

    Args:
        datasets: a list of numpy arrays containing the x and y coordinates of the NVPs
        names: a list of strings containing the names of the datasets
    Returns:
        N/A
    """
    colors = ["#ED037C", "#C0D028", "#00458C", "g", "c", "r"]
    shapes = ["o", "v", "s", "D", "P", "X", "d", "p", "x", "h", "8"]

    fig = plt.figure()
    ax = fig.add_subplot(111)

    num_sets = len(datasets)
    # iterate through each dataset
    for i in range(num_sets):
        # if the corresponding name contains "Ground Truth", make the color black
        # else loop through the colors
        if "Ground Truth" in names[i]:
            color = "#000000"
        else:
            color = colors[i % len(colors)]
        ax.scatter(
            datasets[i][:, 0],
            datasets[i][:, 1],
            s=10,
            c=color,
            marker=shapes[i % len(shapes)],
        )

    ax.grid(True)
    ax.legend(names)
    # Freight Liner Axis Limits
    # ax.set_ylim([-2, 25])
    # Ford Axis Limits
    # ax.set_ylim([-10, 150])
    ax.axvline(x=0, ymin=0, ymax=1, c="k")
    ax.axhline(y=0, xmin=0, xmax=1, c="k")
    # ax.set_title("Freight Liner NVPs with Eye Point as Origin")
    ax.set_title("Ford F450 NVPs with Eye Point as Origin")
    ax.set_xlabel("x-Direction (ft)")
    ax.set_ylabel("y-Direction (ft)")
    ax.axis("square")
    fig.tight_layout()
    plt.show()
