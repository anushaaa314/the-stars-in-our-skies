from pandas import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np 
from astropy.coordinates import get_sun, ICRS
from astropy.time import Time
import astropy.units as u

def mollweide(ra, dec, dist):
    # create plot window
    fig = plt.figure(figsize=(14, 7))
    # create mollweide chart 
    ax = fig.add_subplot(111, projection="mollweide")
    # plot stars by distance, ra, and dec from the perspective of the earth
    scatter = ax.scatter(ra, dec, c=dist, cmap="viridis", 
                        norm=LogNorm(vmin=dist.min(), vmax=dist.max()),
                        s=1, alpha=0.5)
    ax.set_position([0.04, 0.12, 0.80, 0.80])

    # create a bar showing how many parsecs away each color represents
    cbar_ax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    cbar = fig.colorbar(scatter, cax=cbar_ax)
    cbar.set_label("Distance (parsecs)", color="white", fontweight="bold")
    cbar.ax.tick_params(colors="white")

    # retrive sun location 
    time = Time.now()
    # returns sun coordinates in same ICRS reference frame as the star data
    sun = get_sun(time).transform_to(ICRS())
    sun_ra = sun.ra.deg
    sun_dec = sun.dec.deg
    # shift ra range to -180 to 180 for mollweide chart
    sun_ra_shifted = (sun_ra + 180) % 360 - 180
    # convert to radians and get coordinates
    sun_x = np.radians(sun_ra_shifted)
    sun_y = np.radians(sun_dec)

    # plot the sun
    ax.scatter(sun_x, sun_y, color="lemonchiffon", s=180, marker="*", 
               edgecolors="gold", zorder=5)
    ax.annotate("Sun", (sun_x, sun_y), xytext=(8, 8),
                textcoords="offset points", color="lemonchiffon")
    # style the projection
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    # gridlines
    ax.grid(True, color="gray", alpha=0.65)

    ax.set_title("Molleweide map of the stars")
    ax.tick_params(colors="lemonchiffon")

    # top text 
    fig.text(0.5, 0.96, "MOLLWEIDE MAP OF THE STARS", color="white", 
             fontsize="16", fontweight="bold", ha="center")
    fig.text(0.5, 0.93, "Star positions mapped using right acension and declination",
              color="white", fontsize="10", ha="center")
    # bottom text 
    fig.text(0.5, 0.07, "Star colors represent their estimated distance from Earth", 
             color="white", fontsize="10", ha='center')
    fig.text(0.5, 0.035, "Colors use a logarithmic scale", color="white", 
            fontsize=10, ha="center")
    
    plt.show()

def distance_histogram(dist):
    # logarithmically separate distance into 50 bins
    bins = np.logspace(
        np.log10(dist.min()),
        np.log10(dist.max()), 
        51
    )

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111)
    ax.hist(dist, bins=bins, color="mediumpurple", edgecolor="white", alpha=0.85)
    
    ax.set_xscale("log")
    ax.set_title("Distribution of Star Distances")
    ax.set_xlabel("Distance (parsecs)")
    ax.set_ylabel("Number of Stars")

    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.title.set_color("white")

    plt.tight_layout()
    plt.show()


def coordinates_vs_par(ra, dec, par):
    # create a larger plot window
    fig = plt.figure(figsize=(10, 6))
    # two side by side graphs
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # first graph labels
    ax1.scatter(dec, par, color="mediumpurple", s=5, alpha=0.5)
    ax1.set_title("Declination V.S. Parallax")
    ax1.set_xlabel("Declination (degrees: -90 to 90)")
    ax1.set_ylabel("Parallax (milliarcseconds)")

    # second graph labels
    ax2.scatter(ra, par, color="mediumpurple", s=5, alpha=0.5)
    ax2.set_title("Right Ascension V.S. Parallax")
    ax2.set_xlabel("Right Ascension (degrees: 0 - 360)")
    ax2.set_ylabel("Parallax (milliarcseconds)")

    # style both graphs
    for ax in (ax1, ax2):
        ax.set_facecolor("black")
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        ax.grid(True, color="gray", alpha=0.65)

    # black background    
    fig.patch.set_facecolor("black")

    fig.text(0.5, 0.94, "Zoom in!", ha="center", color="white", 
            fontsize=16, fontweight="bold")


    plt.tight_layout()
    plt.show()



# pull data from cleaned csv
stars = read_csv("cleaned_stars.csv")
# get a list of the ra and dec values
ra = stars["ra"]
dec = stars["dec"]
# convert parallax milliarcseconds into parsecs (inverse relationship)
parallax = stars["parallax"]
distance = 1000/parallax

# turn ra range into -180 to 180 
ra_shifted = (ra + 180) % 360 - 180
# degrees to radians 
ra_radians = np.radians(ra_shifted)
dec_radians = np.radians(dec)

print("running...")
print("\nHello!")
print("What kind of star chart would you like to see?\n ")
print("a)   A mollweide projection (an equal-area map that preserves accurate proportions of the " \
"360 degree celestial sphere around us) that 1. plots the directional location of the stars around us using right " \
"acension and declination (a space coordinate system) and 2. color codes their distance from earth.")
print("b)   A histogram that shows how many stars are in different logarithmic distance groups")
print("c)   Two scatterplots, with the first one comparing the declination of a star (what angle up or down a star is from the equator) v.s. " \
"its distance from the earth, and the second comparing the right acension of a star (how many degrees eastward it is from the vernal equinox) v.s. " \
"its distance from the Earth")
while True: 
    graph_choice = input("\na, b, or c?: :  ")
    if graph_choice == "a":
        mollweide(ra=ra_radians, dec=dec_radians, dist=distance)
        break
    elif graph_choice == "b":
        distance_histogram(dist=distance)
        break
    elif graph_choice == "c":
        coordinates_vs_par(ra=ra, dec=dec, par=parallax)
        break
    else:
        print("Please enter one of the letters provided!")