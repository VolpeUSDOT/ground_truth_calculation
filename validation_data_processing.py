import pandas as pd
import matplotlib.pylab as plt
import numpy as np

from data_processing import cart_to_polar

def load_data():
    """
    
    """
    # load and process markerless
    markerless_data_raw = pd.read_csv("./Data/HondaOdysseyFixedInputs.csv")
    markerless_nvp = markerless_data_raw[(abs(markerless_data_raw["x (ft)"]) <= 40) & (abs(markerless_data_raw["y (ft)"]) <= 20)][["x (ft)", "y (ft)"]].to_numpy() - np.array([[1.1155, -7.2507]])
    markerless_nvp = np.concatenate((markerless_nvp, cart_to_polar(markerless_nvp)), axis=1)
    markerless_nvp = markerless_nvp[markerless_nvp[:, 3].argsort()[::-1]]
    
    # load and process view1.0 nvps
    view1_data_raw = pd.read_csv("./Data/HondaOdysseyVIEW1.0.csv")
    view1_nvp = view1_data_raw[view1_data_raw["NVP (in)"] != 379][["x (ft)", "y (ft)"]].to_numpy()
    view1_nvp = np.concatenate((view1_nvp, cart_to_polar(view1_nvp)), axis=1)
    view1_nvp = view1_nvp[view1_nvp[:, 3].argsort()[::-1]]

     # load and process view1.0 nvps
    view1rig_data_raw = pd.read_csv("./Data/HondaOdysseyVIEW1.0Rig.csv")
    view1rig_nvp = view1rig_data_raw[view1rig_data_raw["NVP (in)"] != 438][["x (ft)", "y (ft)"]].to_numpy()
    view1rig_nvp = np.concatenate((view1rig_nvp, cart_to_polar(view1rig_nvp)), axis=1)
    view1rig_nvp = view1rig_nvp[view1rig_nvp[:, 3].argsort()[::-1]]

    # load and process ground truth nvps
    ground_data_raw = pd.read_csv("./Data/HondaOdysseyGroundTruth.csv")
    ground_eye_loc = ground_data_raw[ground_data_raw["Point"] == "Eye"][["x (ft)", "y (ft)"]].to_numpy()
    ground_nvp = ground_data_raw[ground_data_raw["Point"].str.contains("Car|Eye") == False][["x (ft)", "y (ft)"]].to_numpy() - ground_eye_loc
    ground_nvp[:, 1] = ground_nvp[:, 1] * -1
    ground_nvp = np.concatenate((ground_nvp, cart_to_polar(ground_nvp)), axis=1)
    ground_nvp = ground_nvp[ground_nvp[:, 3].argsort()[::-1]]

    return [markerless_nvp, view1_nvp, ground_nvp, view1rig_nvp]

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