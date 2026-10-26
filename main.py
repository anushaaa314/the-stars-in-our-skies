import matplotlib
matplotlib.use("Agg")

from pathlib import Path
from pandas import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap, Normalize
import numpy as np 
from astropy.coordinates import get_sun, ICRS
from astropy.time import Time

BASE_DIR = Path(__file__).resolve().parent

# pull data from cleaned csv
stars = read_csv(BASE_DIR / "cleaned_stars.csv")

# get a list of the ra and dec values
ra = stars["ra"]
dec = stars["dec"]

# turn ra range into -180 to 180 
ra_shifted = (ra + 180) % 360 - 180

# degrees to radians 
ra_radians = np.radians(ra_shifted)
dec_radians = np.radians(dec)

def distance(ra, dec):
    # convert parallax milliarcseconds into parsecs (inverse relationship)
    parallax = stars["parallax"]
    dist = 1000/parallax
    nearby_stars = dist <= 150
    background_stars = dist > 150
    # create plot window
    fig = plt.figure(figsize=(14, 7))
    # create mollweide chart 
    ax = fig.add_subplot(111, projection="mollweide")
    # plot stars by distance, ra, and dec from the perspective of the earth
    scatter = ax.scatter(ra[nearby_stars], dec[nearby_stars], c=dist[nearby_stars], cmap="viridis", 
                        norm=LogNorm(vmin=dist.min(), vmax=dist.max()),
                        s=1, alpha=0.5)
    ax.scatter(ra[background_stars], dec[background_stars], color="gray", s=1,
            alpha=0.5, label="Background stars (>150 parsecs)")
    ax.legend(
    loc="lower left",
    facecolor="black",
    labelcolor="white",
    edgecolor="gray"
    )
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
    fig.text(0.5, 0.96, "DISTANCE OF STARS", color="white", 
             fontsize="16", fontweight="bold", ha="center")
    fig.text(0.5, 0.93, "Star positions mapped using right acension and declination",
              color="white", fontsize="10", ha="center")
    # bottom text 
    fig.text(0.5, 0.07, "Star colors represent their estimated distance from Earth", 
             color="white", fontsize="10", ha='center')
    fig.text(0.5, 0.035, "Colors use a logarithmic scale", color="white", 
            fontsize=10, ha="center")
    
    return fig


def speed(ra, dec):
    pmra = stars["pmra"]
    pmdec = stars["pmdec"]
    angular_speed = np.hypot(pmra, pmdec)

    # create plot window
    fig = plt.figure(figsize=(14, 7))
    # create mollweide chart 
    ax = fig.add_subplot(111, projection="mollweide")
    # plot stars by distance, ra, and dec from the perspective of the earth
    scatter = ax.scatter(ra, dec, c=angular_speed, cmap="viridis", 
                        norm=LogNorm(vmin=angular_speed.min(), vmax=angular_speed.max()),
                        s=1, alpha=0.5)
    ax.set_position([0.04, 0.12, 0.80, 0.80])

    # create a bar showing how many parsecs away each color represents
    cbar_ax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    cbar = fig.colorbar(scatter, cax=cbar_ax)
    cbar.set_label("Angular speed (milliarcseconds/year)", color="white", fontweight="bold")
    cbar.ax.tick_params(colors="white")

    # style the projection
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    # gridlines
    ax.grid(True, color="gray", alpha=0.65)

    ax.set_title("Molleweide map of the stars")
    ax.tick_params(colors="lemonchiffon")

    # top text 
    fig.text(0.5, 0.96, "SPEED OF STARS", color="white", 
             fontsize="16", fontweight="bold", ha="center")
    fig.text(0.5, 0.93, "Star positions mapped using right ascension and declination",
              color="white", fontsize="10", ha="center")
    # bottom text 
    fig.text(0.5, 0.07, "Star colors represent how fast they move across the celestial sphere", 
             color="white", fontsize="10", ha='center')
    fig.text(0.5, 0.035, "Colors use a logarithmic scale", color="white", 
            fontsize=10, ha="center")
    
    return fig

def color(ra, dec):
    # calculate bp and rp color index
    bp = stars["phot_bp_mean_mag"]
    rp = stars["phot_rp_mean_mag"]
    color_index = bp - rp 
    print(color_index.max())
    print(color_index.min())

    # make a custom colormap : blue, white, yellow, orange, red
    star_colors = LinearSegmentedColormap.from_list(
        "star_colors",
        [
            (0.0, "#4E74E8"),
            (0.2, "#ADD8E6"),
            (0.4, "#FFFFFF"),
            (0.55, "#FFFACD"), 
            (0.7, "#FFD700"),  
            (0.82, "#FF8C00"), 
            (1.0, "#B22222")   
        ]
    )

    # normalize color indices using the 1st and 99th percentiles
    vmin = color_index.quantile(0.01)
    vmax = color_index.quantile(0.99)
    color_values = Normalize(vmin=vmin, vmax=vmax, clip=True)(color_index)
    
    # create plot window
    fig = plt.figure(figsize=(14, 7))
    # create mollweide chart 
    ax = fig.add_subplot(111, projection="mollweide")
    # plot stars by distance, ra, and dec from the perspective of the earth
    scatter = ax.scatter(ra, dec, c=color_values, cmap=star_colors,s=2, alpha=0.8, vmin=0, vmax=1)
    ax.set_position([0.04, 0.12, 0.80, 0.80])

    # create a bar showing how many parsecs away each color represents
    cbar_ax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    cbar = fig.colorbar(scatter, cax=cbar_ax)
    cbar.set_label("Approximate BP - RP Color Index", color="white", fontweight="bold")
    cbar.ax.tick_params(colors="white")

    # style the projection
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    # gridlines
    ax.grid(True, color="gray", alpha=0.65)

    ax.set_title("Molleweide map of the stars")
    ax.tick_params(colors="lemonchiffon")

    # top text 
    fig.text(0.5, 0.96, "COLOR OF STARS", color="white", 
             fontsize="16", fontweight="bold", ha="center")
    fig.text(0.5, 0.93, "Star positions mapped using right ascension and declination",
              color="white", fontsize="10", ha="center")
    # bottom text 
    fig.text(0.5, 0.07, "Star colors are estimated from their blue vs red brightness to the Earth", 
             color="white", fontsize="10", ha='center')
    fig.text(0.5, 0.035, "Color index calculated through bluemagnitude minus redmagnitude", color="white", 
            fontsize=10, ha="center")
    
    return fig


def direction(ra, dec):
    pmra = stars["pmra"]
    pmdec = stars["pmdec"]
    ra_angle = np.atan2(pmra, pmdec)
    movement_direction = np.degrees(ra_angle) % 360


    # create plot window
    fig = plt.figure(figsize=(14, 7))
    # create mollweide chart 
    ax = fig.add_subplot(111, projection="mollweide")
    # plot stars by distance, ra, and dec from the perspective of the earth
    scatter = ax.scatter(ra, dec, c=movement_direction, cmap="hsv", vmin=0, vmax=360,
                        s=1, alpha=0.5)
    ax.set_position([0.04, 0.12, 0.80, 0.80])

    # create a bar showing how many parsecs away each color represents
    cbar_ax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    cbar = fig.colorbar(scatter, cax=cbar_ax)
    cbar.set_label("Movement direction Degrees", color="white", fontweight="bold")
    cbar.ax.tick_params(colors="white")
    cbar.set_ticks([0, 90, 180, 270, 360])
    cbar.set_ticklabels(["North (0°)", "East (90°)", "South (180°)", "West (270°)", "North (360°)"])
    
    # style the projection
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    # gridlines
    ax.grid(True, color="gray", alpha=0.65)

    ax.set_title("Molleweide map of the stars")
    ax.tick_params(colors="lemonchiffon")

    # top text 
    fig.text(0.5, 0.96, "DIRECTION OF STARS", color="white", 
             fontsize="16", fontweight="bold", ha="center")
    fig.text(0.5, 0.93, "Star positions mapped using right ascension and declination",
              color="white", fontsize="10", ha="center")
    # bottom text 
    fig.text(0.5, 0.07, "Star colors correlate to what direction a star moves across the celestial sphere", 
             color="white", fontsize="10", ha='center')
    
    return fig


def temp(ra, dec):
    temp = stars["teff_gspphot"]
    vmin = temp.quantile(0.01)
    vmax = temp.quantile(0.99)

    # create plot window
    fig = plt.figure(figsize=(14, 7))
    # create mollweide chart 
    ax = fig.add_subplot(111, projection="mollweide")
    # plot stars by distance, ra, and dec from the perspective of the earth
    scatter = ax.scatter(ra, dec, c=temp, cmap="Reds", norm=Normalize(vmin=vmin, vmax=vmax, clip=True),
                        s=2, alpha=0.8)
    ax.set_position([0.04, 0.12, 0.80, 0.80])

    # create a bar showing how many parsecs away each color represents
    cbar_ax = fig.add_axes([0.90, 0.15, 0.025, 0.70])
    cbar = fig.colorbar(scatter, cax=cbar_ax)
    cbar.set_label("Estimated Effective Temp (K)", color="white", fontweight="bold")
    cbar.ax.tick_params(colors="white")
    
    # style the projection
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")
    # gridlines
    ax.grid(True, color="gray", alpha=0.65)

    ax.set_title("Molleweide map of the stars")
    ax.tick_params(colors="lemonchiffon")

    # top text 
    fig.text(0.5, 0.96, "TEMPERATURE OF STARS", color="white", 
             fontsize="16", fontweight="bold", ha="center")
    fig.text(0.5, 0.93, "Star positions mapped using right ascension and declination",
              color="white", fontsize="10", ha="center")
    # bottom text 
    fig.text(0.5, 0.07, "Darker reds mean hotter temperatures", 
             color="white", fontsize="10", ha='center')
    
    return fig
