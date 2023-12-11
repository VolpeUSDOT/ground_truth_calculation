# Blind Zone Area Calculation

## Description

This code repository is part of [Olin College of Engineering's 2023-2024 Santos-Volpe SCOPE project](https://www.olin.edu/research/view-20-direct-vision-assessment-system).

The purpose of this code is to calculate the blind zone area of a vehicle, given a dataset of nearest visible points (NVPs) for that vehicle.

## Setup

### Dependencies

- [Numpy](https://numpy.org/install/)
- [Matplotlib](https://matplotlib.org/stable/users/installing/index.html)

### Adding Data

1. Save NVP data in a csv file. The data should be in cartesian coordinates, formatted into two columns labeled `x (ft)` and `y (ft)`.
2. Add the csv file into the [`Data`](Data) folder located in the root level of this repository.
3. See the following section for loading the data.

## Usage

Add code to or modify the following files and functions to get a visualization of your NVPs and a value for the blind zone area.

1. In [`data_processing.py`](data_processing.py), modify the function `load_data`.

   - In this function, there are code blocks with structure similar to the following. These are used to load and format NVP data from a csv file and compare them. Modify this function as needed to load the correct datasets. An example template is shown below; replace any all-caps variables with your own.

     ```python
     # load NVPs
     DATA_raw = pd.read_csv(DATA_FILEPATH)
     # extract data from correct columns
     DATA_nvps = DATA_raw[["x (ft)", "y (ft)"]].to_numpy()
     # append column with polar coordinates
     DATA_nvps = np.concatenate((DATA_nvps, cart_to_polar(DATA_nvps)), axis=1)
     # sort by angle - largest to smallest
     DATA_nvps = DATA_nvps[DATA_nvps[:, 3].argsort()[::-1]]
     ```

     Note: More complex data filtering can be done; see [pandas documentation](https://pandas.pydata.org/docs/) or other code blocks in this function for more examples.

   - At the end of this function, modify the variable `datasets` to include only the datasets of interest.

2. In [`compare_nvp_area.py`](compare_nvp_area.py) modify the function `main`.

   - Modify the variable `labels` so that the number and order of the labels match the number and order of the datasets returned from `load_data`.

   - If there is a ground truth dataset included in the list of datasets, make sure that its label contains the string `"Ground Truth"` to ensure that it is recognized as a ground truth dataset.

3. Depending on your Python version, run one of the following commands in the terminal at the root level of this repository to run the code.

   ```batch
   python3 compare_nvp_area.py
   ```

   ```batch
   python compare_nvp_area.py
   ```
