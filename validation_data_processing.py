import pandas as pd
import matplotlib.pylab as plt
import numpy as np

from data_processing import cart_to_polar

def load_data():
    """
    
    """
    # load and process markerless
    markerless_data_raw = pd.read_csv("./Data/HondaOdysseyMarkerless.csv")
    markerless_nvp = markerless_data_raw[["x (ft)", "y (ft)"]].to_numpy() + np.array([[.1115, .725]])
    markerless_nvp = np.concatenate((markerless_nvp, cart_to_polar(markerless_nvp)), axis=1)
    markerless_nvp = markerless_nvp[markerless_nvp[:, 3].argsort()[::-1]]

    # load and process markeless flipped
    markerless_flipped_data_raw = pd.read_csv("./Data/HondaOdysseyMarkerlessXYFlip.csv")
    markerless_flipped_nvp = markerless_flipped_data_raw[["x (ft)", "y (ft)"]].to_numpy() + np.array([[.725, .1115]])
    markerless_flipped_nvp = np.concatenate((markerless_flipped_nvp, cart_to_polar(markerless_flipped_nvp)), axis=1)
    markerless_flipped_nvp = markerless_flipped_nvp[markerless_flipped_nvp[:, 3].argsort()[::-1]]
    
    # load and process view1.0 nvps
    view1_data_raw = pd.read_csv("./Data/HondaOdysseyVIEW1.0.csv")
    view1_nvp = view1_data_raw[view1_data_raw["NVP (in)"] != 379][["x (ft)", "y (ft)"]].to_numpy()
    view1_nvp = np.concatenate((view1_nvp, cart_to_polar(view1_nvp)), axis=1)
    view1_nvp = view1_nvp[view1_nvp[:, 3].argsort()[::-1]]

    # load and process ground truth nvps
    ground_data_raw = pd.read_csv("./Data/HondaOdysseyGroundTruth.csv")
    ground_eye_loc = ground_data_raw[ground_data_raw["Point"] == "Eye"][["x (ft)", "y (ft)"]].to_numpy()
    ground_nvp = ground_data_raw[ground_data_raw["Point"].str.contains("Car|Eye") == False][["x (ft)", "y (ft)"]].to_numpy() - ground_eye_loc
    ground_nvp[:, 1] = ground_nvp[:, 1] * -1
    ground_nvp = np.concatenate((ground_nvp, cart_to_polar(ground_nvp)), axis=1)
    ground_nvp = ground_nvp[ground_nvp[:, 3].argsort()[::-1]]

    return [markerless_nvp, markerless_flipped_nvp, view1_nvp, ground_nvp]

def plot_data(datasets, names):
    """
    
    """
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']
    fig = plt.figure()
    ax = fig.add_subplot(111)

    num_sets = len(datasets)
    for i in range(num_sets):
        ax.scatter(datasets[i][:, 0], datasets[i][:, 1], c=colors[i % len(colors)])
    
    ax.legend(names)
    plt.show()