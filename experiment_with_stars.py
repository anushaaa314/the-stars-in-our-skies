from pandas import *
import matplotlib.pyplot as plt
import numpy as np 
from astropy.coordinates import get_sun
from astropy.time import Time
import astropy.units as u


print("running...")

stars = read_csv("cleaned_stars.csv")
ra = stars["ra"]
dec = stars["dec"]
# turn ra range into -180 to 180 for mollweide graph
ra_shifted = (ra + 180) % 360 - 180
# degrees to radians for mollweide projections
ra_radians = np.radians(ra_shifted)
dec_radians = np.radians(dec)



fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection="mollweide")
ax.scatter(ra_radians, dec_radians, s=1, color="white", alpha=0.5)

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
ax.scatter(sun_x, sun_y, color="lemonchiffon", s=180, marker="*", edgecolors="gold", zorder=5)
ax.annotate("Sun", (sun_x, sun_y), xytext=(8, 8), textcoords="offset points", color="lemonchiffon")

ax.set_facecolor("black")
fig.patch.set_facecolor("black")
ax.grid(True, color="gray", alpha=0.65)

ax.set_title("molleweide map of the stars")
ax.tick_params(colors="yellow")

plt.tight_layout()
plt.show()