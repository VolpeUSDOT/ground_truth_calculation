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

   a.

2. In [`data_processing.py`](data_processing.py), modify the function `plot_data`.

   a.

3. In [`compare_nvp_area.py`](compare_nvp_area.py) modify the function `main`.

   a.
