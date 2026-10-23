from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

OUTPUT_DIR =  Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)
MIN_SAMPLES = 20
MOTION_COLUMNS = ["pmra", "pmdec"]

print("loading the star catalog...")
stars = pd.read_csv("star_clustering/star_data.csv")
stars["source_row"] = np.arange(len(stars))

ra_radians = np.radians(stars["ra"].to_numpy())
dec_radians = np.radians(stars["dec"].to_numpy())
parallax = stars["parallax"]

pmra = stars["pmra"]
pmdec = stars["pmdec"]

sky_x = np.cos(dec_radians) * np.cos(ra_radians)
sky_y = np.cos(dec_radians) * np.sin(ra_radians)
sky_z = np.sin(dec_radians)

scaler = StandardScaler()
X = scaler.fit_transform(stars[MOTION_COLUMNS])
print("features used to find clusters: pmra, pmdec")

neighbors = NearestNeighbors(n_neighbors=MIN_SAMPLES, n_jobs=-1)
neighbors.fit(X)

distances, neighbor_indices = neighbors.kneighbors(X)
k_distances = np.sort(distances[:, -1])

plt.figure(figsize=(10, 6))
plt.plot(k_distances)
plt.title(f"K-Distance Plot (k - {MIN_SAMPLES})")
plt.xlabel("Stars, sorted by distance")
plt.ylabel("Distance to 20th nearest neighbor")
plt.grid(True, alpha=0.3)
plt.savefig(OUTPUT_DIR / "k_distance_plot.png", dpi=200)
plt.show()

zoom_limit = np.percentile(k_distances, 99)
plt.figure(figsize=(10, 6))
plt.plot(k_distances)
plt.title("Zoomed K-Distance Plot (Lower 99%)")
plt.xlabel("Stars, sorteed by distance")
plt.ylabel("Distance to 20th nearest neighbor")
plt.ylim(0, zoom_limit)
plt.grid(True, alpha=0.3)
plt.savefig(OUTPUT_DIR / "k_zoomed_distance_plot.png", dpi=200)
plt.tight_layout()
plt.show()