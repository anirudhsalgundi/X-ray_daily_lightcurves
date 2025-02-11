from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.simbad import Simbad
import numpy as np
import pandas as pd
import argparse
import matplotlib.pyplot as plt

def get_maxi_id(source_name):
    print(f"Getting Coordinates for {source_name} from SIMBAD ... This may take a minute or two.")


    object_id = Simbad.query_object(source_name)
    coord = SkyCoord(ra=object_id['ra'], dec=object_id['dec'], unit=(u.hourangle, u.deg), frame='icrs')
    ra_str = coord.ra.to_string(unit=u.hour, sep="", precision=2, pad=True)
    dec_str = coord.dec.to_string(unit=u.degree, sep="", precision=2, alwayssign=True, pad=True)

    ra_print = coord.ra.to_string(unit=u.hour, sep=":", precision=2, pad=True)
    dec_print = coord.dec.to_string(unit=u.degree, sep=":", precision=2, alwayssign=True, pad=True)

    print(f"Found {source_name} at RA: {ra_print[0]} and Dec: {dec_print[0]}!!")
    print("Fetching MAXI data ...")
    return f"{ra_str[0][0:4]}{dec_str[0][0:3]}{dec_str[0][4]}"

def fetch_maxi_data(maxi_id):
    url = f"http://maxi.riken.jp/star_data/J{maxi_id}/J{maxi_id}_g_lc_1day_all.dat" 
    data = pd.read_csv(url, sep=r" ", header=None)
    data.columns = ["MJD", "2-20keV", "2-20keV_err", "2-4keV", "2-4keV_err", "4-10keV", "4-10keV_err", "10-20keV", "10-20keV_err"]
    return data, url


def plot_light_curve(ax, x, y, yerr, color, label):
    ax.errorbar(x, y, yerr=yerr, fmt=' ', markersize=2, color=color, ecolor=color, elinewidth=0.8, capsize=1.5, alpha=0.5)
    ax.errorbar(x, y, fmt = 'o',  markersize=2, color=color, ecolor=color, alpha=1)
    ax.set_ylabel(label, fontsize=14)
    ax.tick_params(labelsize=12)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.6)

def plot_maxi_lc():
    data, url = fetch_maxi_data(maxi_id)
    if data is None:
        return  # Exit if data fetch failed
    
    print(f"Data fetched from {url}")

    energy_bands = [
        ("2-4keV", "2-4keV_err", "C0"),
        ("4-10keV", "4-10keV_err", "C1"),
        ("10-20keV", "10-20keV_err", "C2"),
        ("2-20keV", "2-20keV_err", "C3")
    ]

    fig, axes = plt.subplots(len(energy_bands))

    for ax, (y_col, yerr_col, color) in zip(axes, energy_bands):
        plot_light_curve(ax, data["MJD"], data[y_col], data[yerr_col], color, y_col)
        if ax != axes[-1]:
            ax.set_xticklabels([])
        else:
            pass


    axes[0].set_title(f"MAXI Light Curve for {source_name}")
    axes[-1].set_xlabel("MJD")
    
    plt.subplots_adjust(hspace=0.0)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot MAXI light curve for a given source.")
    parser.add_argument("-s", "--source", type=str, required=True, help="Name of the source")
    args = parser.parse_args()
    
    source_name = args.source
    maxi_id = get_maxi_id(source_name)

    if maxi_id:
        plot_maxi_lc()
    else:
        print(f"Error: Could not retrieve MAXI ID for {source_name}.")