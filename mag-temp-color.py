from pandas import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np 
from astropy.coordinates import get_sun, ICRS
from astropy.time import Time

# pull data from cleaned csv
stars = read_csv("cleaned_stars.csv")

def colorindex_temp(stars):
    # getting temp and calc color index
    effec_temp = stars["teff_gspphot"]
    color_index = stars["phot_bp_mean_mag"] - stars["phot_rp_mean_mag"]

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111)
    scatter = ax.scatter(color_index, effec_temp, c=effec_temp, 
        cmap="coolwarm", s=3, alpha=0.5)

    ax.set_xlabel("BP - RP Color Index")
    ax.set_ylabel("Effective Temperature (K)")
    ax.set_title("Stellar Temperature V.S. Color")

    fig.colorbar(scatter, ax=ax, label="Temperature (K)")
    ax.grid(True, alpha=0.4)
    plt.tight_layout
    plt.show()

colorindex_temp(stars=stars)

def hr_diagram(stars):
    