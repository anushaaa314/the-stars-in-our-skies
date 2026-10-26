
from io import BytesIO
from threading import Lock

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from flask import Flask, abort, render_template, send_file

import main


app = Flask(__name__)

# Prevent multiple requests from manipulating Matplotlib
# figures simultaneously.
plot_lock = Lock()


# Connect each URL name to its plotting function and description.
PLOTS = {
    "distance": {
        "title": "Distance of Stars",
        "description": "Estimated distance from Earth in parsecs.",
        "function": main.distance,
        "explanation": """
        - A parsec is a unit of astronomical distance equal to about 3.26 light years and it is calculated using a star's parallax. Parallax is the 
        apparent shift in a star's position as earth revolves around the sun (see picture below). The distance in parsecs is normally calculated by 
        taking the reciprocal of the parallax (distance = 1/parallax), when parallax is measured in arcseconds. However, the Gaia Dr3 dataset 
        measures parallax in milliarcseconds, so the formula becomes distance = 1000/parallax. 
        - The colors use a logarithmic scale, so the stars may appear the same color. However, if you look closely, you can see various shades of blue 
        as well as many yellow outliers
        - I would like to clarify that the earth is not near the sun at all in this projection. If you wrap this 2D projection back into it's 3D 360 degree 
        shape, the Earth will actually be in the center of, or inside, the sphere. We are the stationary observer watching the objects in the sphere move 
        around us. 
        """
    },
    "speed": {
        "title": "Speed of Stars",
        "description": "Angular speed across the celestial sphere.",
        "function": main.speed,
        "explanation": """
        The speeds graphed are derived from the proper motion of these stars. 
        Proper motion describes how a star appers to move across the sky over time. It is measured in milliarcseconds/year.
        The Gaia Dr3 dataset meausres this motion in two directions: 
            - pmra: motion along the right ascension direction, adjusted by
        the cosine of the declination.
            - pmdec: motion along the declination direction.
        Pmra and pmdec are perpendicular motion components. The overall angular speed is calculated using the Pythagorean theorm:
        speed = sqrt(pmra² + pmdec²)
        This only describes how fast a star's apparent motion is across the night sky, not its full 3D velocity through space. 
        """
    },
    "color": {
        "title": "Color of Stars",
        "description": "Star color index calculated using BP - RP.",
        "function": main.color,
        "explanation": """"
        -   This projection uses a BP - RP color index from the Gaia Dr3 catalog. Gaia has two photometers that measure light in different wavelength range. 
        A tool called a Blue Photometer measures the bluer part of a star's wavelength while a Red Photometer measures the red one. Each produces a brightness
        measurement called magniture. The color
        index is calculated by subtracting the RP magnitude from the BP
        magnitude:
        BP - RP = BP magnitude - RP magnitude

        - A lower, sometimes negative, value generally indicates a bluer star, while a higher value generally indicates a redder star. The index is
        a useful indicator of stellar color, but it can also be affected by dust between the star and Earth.
        
        """
    },
    "direction": {
        "title": "Direction of Stars",
        "description": "Direction of stellar proper motion.",
        "function": main.direction,
        "explanation": """
        This chart uses the columns pmra and pmdec from the Gaia Dr3 dataset.
            - pmra describes the star's apparent motion along the right ascension
            direction.
            - pmdec describes its apparent motion along the declination direction.

        The direction angle is calculated from these two components using the arctangent function (atan2). This determines the angle of the motion vector while 
        also accounting for which components are positive or negative.
        The angle describes the direction the star appears to move across
        the sky. It does not, by itself at least , convey the star's full direction
        of travel through 3D space.

        """
    },
    "temp": {
        "title": "Temperature of Stars",
        "description": "Estimated stellar effective temperature.",
        "function": main.temp,
        "explanation": """
        The temperature shown is the estimatated effective temperature of each star
        Effective temperature is the temperature a theoretical blackbody would need to have to emit the same total energy per unit surface
        area as the star.


        """
    },
}


# Homepage: display all five visualization options.
@app.route("/")
def home():
    return render_template("index.html", plots=PLOTS)


# Plot page: display the title, description, and image.
@app.route("/plot/<plot_name>")
def show_plot(plot_name):
    if plot_name not in PLOTS:
        abort(404)

    return render_template(
        "plot.html",
        plot_name=plot_name,
        plot=PLOTS[plot_name],
        plots=PLOTS,
    )


# Image endpoint: generate the selected plot and return a PNG.
@app.route("/image/<plot_name>")
def plot_image(plot_name):
    if plot_name not in PLOTS:
        abort(404)

    plot_info = PLOTS[plot_name]

    with plot_lock:
        # Call the selected function from main.py.
        fig = plot_info["function"](
            ra=main.ra_radians,
            dec=main.dec_radians,
        )

        image_buffer = BytesIO()

        try:
            fig.savefig(
                image_buffer,
                format="png",
                dpi=120,
                bbox_inches="tight",
                facecolor=fig.get_facecolor(),
            )
        finally:
            plt.close(fig)

        image_buffer.seek(0)

    return send_file(
        image_buffer,
        mimetype="image/png",
        download_name=f"{plot_name}.png",
    )


# Start the development server when running this file directly.
if __name__ == "__main__":
    app.run(debug=True)
