import pandas as pd # type: ignore
import argparse
import matplotlib.pyplot as plt # type: ignore

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
    Plots the Swift/BAT light curve data in a publication-quality format.
    """
    # Extract columns
    mask = data[1] > 0  # Filter negative count rates
    time = data[0][mask]
    rate = data[1][mask]
    error = data[2][mask]

    # Set up figure and axes
    fig, ax = plt.subplots()  # High resolution

    # Plot error bars with transparency
    ax.errorbar(time, rate, yerr=error, fmt=" ", 
                elinewidth=0.8, capsize=1.2, capthick=0.8, alpha=0.4, color="C3")
    
    # Plot data points with higher opacity
    ax.errorbar(time, rate, fmt="o", ms=2, color="C3", alpha=1, label="Swift/BAT Data")

    # Axis labels
    ax.set_xlabel("Time (MJD)", fontsize=14, fontweight='bold')
    ax.set_ylabel("Count Rate (12-50 keV)", fontsize=14, fontweight='bold')

    # Title
    ax.set_title(f"Swift/BAT Light Curve of {source_name}", fontsize=15, fontweight='bold')

    # Aesthetic improvements
    ax.tick_params(axis="both", which="major", labelsize=12, direction="in", length=5)
    ax.tick_params(axis="both", which="minor", direction="in", length=3)
    ax.minorticks_on()
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.6)

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