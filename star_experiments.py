from pandas import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np 
from astropy.coordinates import get_sun
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
    sun = get_sun(time)
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
        50
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

def three_d_model(ra, dec, dist):
    # convert spherical coordinates into 3d cartesian coordinates
    # because we can't plot degrees (dec/ra)
    x = dist * np.cos(dec) * np.cos(ra)
    y = dist * np.cos(dec) * np.sin(ra)
    z = dist * np.sin(dec)

    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection="3d")
    scatter = ax.scatter(x, y, z, c=dist, cmap="viridis", 
                         norm=LogNorm(vmin=dist.min(), vmax=dist.max()), 
                         s=3, alpha=0.7)
    ax.set_xlabel("X (parsecs)")
    ax.set_ylabel("Y (parsecs)")
    ax.set_zlabel("Z (parsecs)")
    ax.set_title("3D Map of Stars")

    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.tick_params(colors="black", labelsize=8)
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    ax.zaxis.label.set_color("white")
    ax.title.set_color("white")

    # make 3 axes, equal visual scaling
    ax.set_box_aspect((1, 1, 1))

    plt.tight_layout()
    plt.show()



# pull data from cleaned csv
stars = read_csv("cleaned_stars.csv")
# get a list of the ra and dec values
ra = stars["ra"]
dec = stars["dec"]
# convert parallax milliarcseconds into parsecs (inverse relationship)
distance = 1000/stars["parallax"]

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
while True: 
    graph_choice = input("\na, b, c, or d?:  ")
    if graph_choice == "a":
        mollweide(ra=ra_radians, dec=dec_radians, dist=distance)
        break
    elif graph_choice == "b":
        distance_histogram(dist=distance)
        break
    elif graph_choice == "c":
        three_d_model(ra_radians, dec_radians, distance)
        break
    else:
        print("Please enter one of the letters provided!")