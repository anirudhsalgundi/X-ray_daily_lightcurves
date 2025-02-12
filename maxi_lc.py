from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def get_maxi_id(source_name):
    """
    Given a source name, this function queries the SIMBAD database to get the coordinates of the source nad retuen the MAXI ID for the source.
    MAXI ID is J{RA}{Dec} where RA and Dec are the coordinates of the source in the format HHMM+DDdMMm
    MAXI ID is needed to fetch the light curve data from the MAXI online database.
    We dont have to downlaod any data
    """
    print(f"Getting Coordinates for {source_name} from SIMBAD ... This may take a minute or two.")

    #Perform a SIMBAD query to get the coordinates of the source
    object_id = Simbad.query_object(source_name)

    #Define the coordinates of the source
    coord = SkyCoord(ra=object_id['ra'], dec=object_id['dec'], unit=(u.hourangle, u.deg), frame='icrs')

    #Convert the coordinates to a string format that can be used to fetch MAXI data
    ra_str = coord.ra.to_string(unit=u.hour, sep="", precision=2, pad=True)
    dec_str = coord.dec.to_string(unit=u.degree, sep="", precision=2, alwayssign=True, pad=True)

    #coordinates of the source that can be used for prinitng in the terminal
    ra_print = coord.ra.to_string(unit=u.hour, sep=":", precision=2, pad=True)
    dec_print = coord.dec.to_string(unit=u.degree, sep=":", precision=2, alwayssign=True, pad=True)
    print(f"Found {source_name} at RA: {ra_print[0]} and Dec: {dec_print[0]}!!")

    #Return the MAXI ID for the source
    print("Fetching MAXI data ...")
    return f"{ra_str[0][0:4]}{dec_str[0][0:4]}"

def fetch_maxi_data(maxi_id):
    """
    Given a MAXI ID, this function fetches the light curve data for the source from the MAXI online database, by querying the URL for the source.
    """

    #Create the URL for the source
    url = f"http://maxi.riken.jp/star_data/J{maxi_id}/J{maxi_id}_g_lc_1day_all.dat" 

    #Try to fetch the data from the URL
    data = pd.read_csv(url, sep=r" ", header=None)
    data.columns = ["MJD", "2-20keV", "2-20keV_err", "2-4keV", "2-4keV_err", "4-10keV", "4-10keV_err", "10-20keV", "10-20keV_err"]

    #Return the data and the URL
    return data, url


def plot_light_curve(ax, x, y, yerr, color, label):
    """
    Standard function to plot a light curve with error bars
    """
    ax.errorbar(x, y, yerr=yerr, fmt=' ', markersize=2, color=color, ecolor=color, elinewidth=0.8, capsize=1.5, alpha=0.5)
    ax.errorbar(x, y, fmt = 'o',  markersize=2, color=color, ecolor=color, alpha=1)
    ax.set_ylabel(label, fontsize=14)
    ax.tick_params(labelsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)

def plot_maxi_lc():
    """
    Main function to plot the MAXI light curve for a given source. This runs the function fetch_maxi_data() to get the data and then plots the light curve.
    """
    data, url = fetch_maxi_data(maxi_id)
    if data is None:
        return  # Exit if data fetch failed
    
    #Print the URL from which the data was fetched
    print(f"Data fetched from {url}")

    #Define the energy bands and the colors for the light curve plot
    energy_bands = [
        ("2-4keV", "2-4keV_err", "C0"),
        ("4-10keV", "4-10keV_err", "C1"),
        ("10-20keV", "10-20keV_err", "C2"),
        ("2-20keV", "2-20keV_err", "C3")
    ]

    #Plot the light curve for each energy band
    fig, axes = plt.subplots(len(energy_bands))

    for ax, (y_col, yerr_col, color) in zip(axes, energy_bands):
        plot_light_curve(ax, data["MJD"], data[y_col], data[yerr_col], color, y_col)
        if ax != axes[-1]:
            ax.set_xticklabels([])
        else:
            pass

    #Set the title and labels for the plot
    axes[0].set_title(f"MAXI Light Curve for {source_name}")
    axes[-1].set_xlabel("MJD")
    
    #Adjust the plot layout by leaving no space between the subplots
    plt.subplots_adjust(hspace=0.0)

    #Show the plot
    plt.show()



# Main function to run the script
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot MAXI light curve for a given source.")
    #Add argyments to the parser. -s or --source is required
    parser.add_argument("-s", "--source", type=str, required=True, help="Name of the source")
    args = parser.parse_args()
    source_name = args.source
    maxi_id = get_maxi_id(source_name)
    plot_maxi_lc()