import pandas as pd
import matplotlib.pylab as plt
import numpy as np

from data_processing import cart_to_polar, get_intersection

def load_data():
    """
    
    """
    # load and process markerless
    markerless_data_raw = pd.read_csv("./Data/HondaOdysseyMarkerless.csv")
    markerless_nvp = markerless_data_raw[(abs(markerless_data_raw["x (ft)"]) <= 40) & (abs(markerless_data_raw["y (ft)"]) <= 20)][["x (ft)", "y (ft)"]].to_numpy() - np.array([[1.1155, -7.2507]])
    markerless_nvp = np.concatenate((markerless_nvp, cart_to_polar(markerless_nvp)), axis=1)
    markerless_nvp = markerless_nvp[markerless_nvp[:, 3].argsort()[::-1]]

    # load and process markerless with rig
    markerlessrig_data_raw = pd.read_csv("./Data/HondaOdysseyMarkerlessRig.csv")
    markerlessrig_nvp = markerlessrig_data_raw[(abs(markerlessrig_data_raw["x (ft)"]) <= 40) & (abs(markerlessrig_data_raw["y (ft)"]) <= 20)][["x (ft)", "y (ft)"]].to_numpy() - np.array([[1.8542, -7.5208]])
    markerlessrig_nvp = np.concatenate((markerlessrig_nvp, cart_to_polar(markerlessrig_nvp)), axis=1)
    markerlessrig_nvp = markerlessrig_nvp[markerlessrig_nvp[:, 3].argsort()[::-1]]
    
    # load and process view1.0 nvps
    view1_data_raw = pd.read_csv("./Data/HondaOdysseyVIEW1.0.csv")
    view1_nvp = view1_data_raw[view1_data_raw["NVP (in)"] != 379][["x (ft)", "y (ft)"]].to_numpy()
    view1_nvp = np.concatenate((view1_nvp, cart_to_polar(view1_nvp)), axis=1)
    view1_nvp = view1_nvp[view1_nvp[:, 3].argsort()[::-1]]

     # load and process view1.0 rig nvps
    view1rig_data_raw = pd.read_csv("./Data/HondaOdysseyVIEW1.0Rig.csv")
    view1rig_nvp = view1rig_data_raw[view1rig_data_raw["NVP (in)"] != 438][["x (ft)", "y (ft)"]].to_numpy()
    view1rig_nvp = np.concatenate((view1rig_nvp, cart_to_polar(view1rig_nvp)), axis=1)
    view1rig_nvp = view1rig_nvp[view1rig_nvp[:, 3].argsort()[::-1]]

    # load and process lidar nvps with rig setup
    lidarrig_data_raw = pd.read_csv("./Data/HondaOdysseyLidarRig.csv")
    lidarrig_nvp = lidarrig_data_raw[["x (ft)", "y (ft)"]].to_numpy()
    lidarrig_nvp = np.concatenate((lidarrig_nvp, cart_to_polar(lidarrig_nvp)), axis=1)
    lidarrig_nvp = lidarrig_nvp[lidarrig_nvp[:, 3].argsort()[::-1]]

    # load and process ground truth nvps
    ground_data_raw = pd.read_csv("./Data/HondaOdysseyGroundTruth.csv")
    ground_eye_loc = ground_data_raw[ground_data_raw["Point"] == "Eye"][["x (ft)", "y (ft)"]].to_numpy()
    ground_nvp = ground_data_raw[ground_data_raw["Point"].str.contains("Car|Eye") == False][["x (ft)", "y (ft)"]].to_numpy() - ground_eye_loc
    ground_nvp[:, 1] = ground_nvp[:, 1] * -1
    ground_nvp = np.concatenate((ground_nvp, cart_to_polar(ground_nvp)), axis=1)
    ground_nvp = ground_nvp[ground_nvp[:, 3].argsort()[::-1]]

    # load and process ground truth rig nvps
    groundrig_data_raw = pd.read_csv("./Data/HondaOdysseyGroundTruthRig.csv")
    groundrig_eye_loc = groundrig_data_raw[groundrig_data_raw["Point"] == "Eye"][["x (ft)", "y (ft)"]].to_numpy()
    groundrig_nvp = groundrig_data_raw[groundrig_data_raw["Point"] == "Car"][["x (ft)", "y (ft)"]].to_numpy() - groundrig_eye_loc
    groundrig_nvp[:, 1] = groundrig_nvp[:, 1] * -1
    groundrig_nvp = np.concatenate((groundrig_nvp, cart_to_polar(groundrig_nvp)), axis=1)
    groundrig_nvp = groundrig_nvp[groundrig_nvp[:, 3].argsort()[::-1]]

    # datasets = [markerless_nvp, view1_nvp, ground_nvp, markerlessrig_nvp, view1rig_nvp, lidarrig_nvp, groundrig_nvp]
    datasets = [markerlessrig_nvp, view1rig_nvp, lidarrig_nvp, groundrig_nvp]
    left_bound, right_bound = get_left_and_right_bound(datasets)

    return trim_datasets(datasets, left_bound, right_bound)

def get_left_and_right_bound(datasets):
    """
    
    """
    leftmost_points = [dataset[0, :] for dataset in datasets]
    rightmost_points = [dataset[-1, :] for dataset in datasets]

    left = min(leftmost_points, key=lambda x: x[3])
    right = max(rightmost_points, key=lambda x: x[3])

    return left, right

def trim_datasets(datasets, left_bound, right_bound):
    """
    
    """
    res = []
    for dataset in datasets:
        if not np.array_equal(dataset[0, :], left_bound):
            left_ind = None
            for i, point in enumerate(dataset):
                if left_ind is None or point[3] > left_bound[3]:
                    left_ind = i
                else:
                    break
        else:
            left_ind = 0
        
        if not np.array_equal(dataset[-1, :], right_bound):
            right_ind = None
            for i, point in enumerate(dataset[::-1]):
                if right_ind is None or point[3] < right_bound[3]:
                    right_ind = len(dataset) - i
                else:
                    break
        else:
            right_ind = -1

        new_dataset = dataset[left_ind:right_ind, :]
        if not np.array_equal(dataset[0, :], left_bound):
            new_dataset[0, :] = get_intersection(new_dataset[0:2, :], left_bound)
        if not np.array_equal(dataset[-1, :], right_bound):
            new_dataset[-1, :] = get_intersection(new_dataset[-2:, :], right_bound)
        res.append(new_dataset)

    return res
            

def plot_data(datasets, names):
    """
    
    """
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    fig = plt.figure()
    ax = fig.add_subplot(111)

    num_sets = len(datasets)
    for i in range(num_sets):
        ax.scatter(datasets[i][:, 0], datasets[i][:, 1], c=colors[i % len(colors)])
    
    ax.axvline(x=0, ymin=0, ymax=1, c="k")
    ax.axhline(y=0, xmin=0, xmax=1, c="k")
    ax.set_title("NVPs with Eye Point as Origin")
    ax.set_xlabel("x-Direction (ft)")
    ax.set_ylabel("y-Direction (ft)")
    ax.legend(names)
    fig.tight_layout()
    plt.show()