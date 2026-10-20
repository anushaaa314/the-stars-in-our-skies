from pandas import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np 
from astropy.coordinates import get_sun
from astropy.time import Time
import astropy.units as u


print("running...")

# pull data from cleaned csv
stars = read_csv("cleaned_stars.csv")
# get a list of the ra and dec values
ra = stars["ra"]
dec = stars["dec"]
# convert parallax milliarcseconds into parsecs (inverse relationship)
distance = 1000/stars["parallax"]

# turn ra range into -180 to 180 for mollweide graph
ra_shifted = (ra + 180) % 360 - 180
# degrees to radians for mollweide projections
ra_radians = np.radians(ra_shifted)
dec_radians = np.radians(dec)

# create plot window
fig = plt.figure(figsize=(14, 7))
# create mollweide chart 
ax = fig.add_subplot(111, projection="mollweide")
# plot stars by distance, ra, and dec from the perspective of the earth
scatter = ax.scatter(ra_radians, dec_radians, c=distance, cmap="viridis", 
                    norm=LogNorm(vmin=distance.min(), vmax=distance.max()),
                    s=0.5, alpha=0.5)
ax.set_position([0.04, 0.12, 0.80, 0.80])

# create a bar showing how many parsecs away each color represents
cbar_ax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
cbar = fig.colorbar(scatter, cax=cbar_ax)
cbar.set_label("Distance (parsecs)", color="white")
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

ax.set_facecolor("black")
fig.patch.set_facecolor("black")
ax.grid(True, color="gray", alpha=0.65)

ax.set_title("molleweide map of the stars")
ax.tick_params(colors="yellow")


plt.show()