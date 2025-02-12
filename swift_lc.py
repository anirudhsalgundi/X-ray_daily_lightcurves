from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def get_swift_data(source_name):
    """
    Fetches the Swift/BAT light curve data for a given source from NASA's database.
    Returns the dataframe if successful, else None.
    """
    # Normalize source name (remove spaces)
    source_id = source_name.replace(" ", "")
    
    # Possible URLs
    urls = [
        f"https://swift.gsfc.nasa.gov/results/transients/weak/{source_id}.lc.txt",
        f"https://swift.gsfc.nasa.gov/results/transients/{source_id}.lc.txt"
    ]

    for url in urls:
        try:
            data = pd.read_csv(url, sep=r"\s+", skiprows=5, header=None)
            print(f"Successfully fetched data from {url}")
            return data  # Return dataframe instead of URL
        except:
            print(f"The URL {url} did not work. Trying a different one.")
            pass

    print(f"Could not fetch data for {source_name}.")
    return None  # Return None if both URLs fail


def plot_swift_lc(data, source_name):
    """
    Plots the Swift/BAT light curve data.
    """
    # Extract columns
    mask = data[1] > 0  # Remove negative times
    time = data[0][mask]
    rate = data[1][mask]
    error = data[2][mask]

    # Plot
    fig, ax = plt.subplots()
    ax.errorbar(time, rate, yerr=error, fmt=".", ms = 1, elinewidth=1, capsize=0.5, c = "C3", alpha = 0.5)
    ax.errorbar(time, rate, fmt=".", ms = 1, c = "C3", alpha = 1)
    ax.set_xlabel("Time (MJD)")
    ax.set_ylabel("Count Rate (12.0 - 50.0 keV)")
    plt.title(f"Swift/BAT Light Curve of {source_name}")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot MAXI light curve for a given source.")
    parser.add_argument("-s", "--source", type=str, required=True, help="Name of the source")
    args = parser.parse_args()

    source_name = args.source
    swift_data = get_swift_data(source_name)

    if swift_data is not None:
        plot_swift_lc(swift_data, source_name) # Check first few rows
    else:
        print("No data available.")