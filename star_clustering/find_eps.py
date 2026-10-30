from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from kneed import KneeLocator


from sklearn.cluster import DBSCAN
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler


OUTPUT_DIR =  Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)
MIN_SAMPLES = 20
MOTION_COLUMNS = ["pmra", "pmdec"]


print("loading the star catalog...")
star = pd.read_csv("star_clustering/star_data.csv")
stars = star[["ra", "parallax", "dec", "pmra", "pmdec"]].copy()


ra_radians = np.radians(stars["ra"].to_numpy())
dec_radians = np.radians(stars["dec"].to_numpy())
parallax = stars["parallax"]


pmra = stars["pmra"]
pmdec = stars["pmdec"]


sky_x = np.cos(dec_radians) * np.cos(ra_radians)
sky_y = np.cos(dec_radians) * np.sin(ra_radians)
sky_z = np.sin(dec_radians)


stars["sky_x"] = sky_x
stars["sky_y"] = sky_y
stars["sky_z"] = sky_z


experiments = {
    "motion": ["pmra", "pmdec"],
    "motion_sky_parallax": ["pmra", "pmdec", "sky_x", "sky_y", "sky_z", "parallax"]
}


scaled_features = {}
for name, features in experiments.items():
    print("\npreparing...")
    scaler = StandardScaler()
    X = scaler.fit_transform(stars[features])
    scaled_features[name] = X


    neighbors = NearestNeighbors(n_neighbors=MIN_SAMPLES+1, n_jobs=-1)
    neighbors.fit(X)


    distances, _ = neighbors.kneighbors(X)
    k_distances = np.sort(distances[:, -1])


    plt.figure(figsize=(10, 6))
    plt.plot(np.arange(len(k_distances)), k_distances)
    plt.title(f"K-Distance Plot - {name.upper()} (k - {MIN_SAMPLES})")
    plt.xlabel("Stars, sorted by distance")
    plt.ylabel("Distance to 20th nearest neighbor")
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / f"{name}_k_distance_plot.png", dpi=200)
    plt.show()


    cutoff = int(len(k_distances) * 0.95)
    k_distances_zoomed = k_distances[:cutoff]
    x_values = np.arange(len(k_distances_zoomed))


    plt.figure(figsize=(10, 6))
    plt.plot(k_distances_zoomed)
    plt.title(f"Zoomed K-Distance Plot - {name.upper()} (Lower 99%)")
    plt.xlabel("Stars, sorteed by distance")
    plt.ylabel("Distance to 20th nearest neighbor")
    plt.grid(True, alpha=0.3)
    plt.savefig(OUTPUT_DIR / f"{name}_k_zoomed_plot.png", dpi=200)
    plt.tight_layout()
    plt.show()


    knee_finder = KneeLocator(x_values, k_distances_zoomed
                              , curve="convex",
        direction="increasing", S=1.0)


    if knee_finder.knee is None:
        print("No clear knee detected. ")
    else:
        eps_candidate = float(knee_finder.knee_y)
        print(f"detected knee index: {knee_finder.knee}" )
        print(f"Estimated eps: {eps_candidate}")


        plt.figure(figsize=(10, 6))
        plt.plot(x_values, k_distances_zoomed, label="K-distance curve")
        plt.axvline(
            knee_finder.knee,
            color="red",
            linestyle="--",
            label="Detected knee"
        )
        plt.axhline(
            eps_candidate,
            color="green",
            linestyle="--",
            label=f"Candidate eps = {eps_candidate:.4f}"
        )


        plt.title("Automatic K-Distance Knee Detection")
        plt.xlabel("Stars, sorted by distance")
        plt.ylabel("Distance to 20th nearest neighbor")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / f"{name}_automatic_knee.png", dpi=200)
        plt.show()


eps_values = {}
for name in experiments:
    answer = float(input(f"Enter eps for {name}: "))
    eps_values[name] = answer


cluster_results = {}
summary_rows = []
for name, X in scaled_features.items():
    eps = eps_values[name]
    print("running DBSCAN...")


    model = DBSCAN(eps=eps, min_samples=MIN_SAMPLES)
    labels = model.fit_predict(X)
    result = stars.copy()
    result["cluster"] = labels
    cluster_results[name] = result


    unique_labels = set(labels)
    clusters = sorted(
        label for label in unique_labels
        if label != -1
    )
   
    noise_count = int(np.sum(labels == -1))
    noise_frac = noise_count/len(labels)
    print("Clusters found:", len(clusters))
    print("Noise stars:", noise_count)
    print(f"Noise fraction: {noise_frac:.1%}")
    output_csv = OUTPUT_DIR / f"{name}_clusters.csv"
    result.to_csv(output_csv, index=False)




    for cluster_id, group in result.groupby("cluster"):
        summary_rows.append({
            "model": name,
            "cluster": int(cluster_id),
            "n_stars": len(group),
            "median_ra": group["ra"].median(),
            "median_dec": group["dec"].median(),
            "median_parallax": group["parallax"].median(),
            "median_pmra": group["pmra"].median(),
            "median_pmdec": group["pmdec"].median(),
            "is_noise": cluster_id == -1
        })


summary = pd.DataFrame(summary_rows)
summary_path = OUTPUT_DIR / "cluster_summary.csv"
summary.to_csv(summary_path, index=False)
print(f"\nSaved cluster summary: {summary_path}")


for name, result in cluster_results.items():
    fig = plt.figure(figsize=(12, 6))
    ax = fig.add_subplot(111, projection="mollweide")


    labels = result["cluster"].to_numpy()
    noise = labels == -1
    clustered = ~noise


    # Convert celestial coordinates to radians
    ra_rad = np.radians(result["ra"].to_numpy())
    dec_rad = np.radians(result["dec"].to_numpy())


    # Reverse RA so it increases from right to left
    longitude = -ra_rad
    longitude = (longitude + np.pi) % (2 * np.pi) - np.pi


    # Draw noise stars in gray
    ax.scatter(
        longitude[noise],
        dec_rad[noise],
        s=2,
        color="lightgray",
        alpha=0.4,
        label="Noise",
        rasterized=True
    )


    # Draw clustered stars, colored by DBSCAN label
    if clustered.any():
        ax.scatter(
            longitude[clustered],
            dec_rad[clustered],
            c=labels[clustered],
            cmap="tab20",
            s=5,
            alpha=0.85,
            label="Clustered stars",
            rasterized=True
        )


    ax.grid(True, alpha=0.3)
    ax.set_xlabel("Right ascension")
    ax.set_ylabel("Declination")
    ax.set_title(f"Mollweide Sky Map — {name}")
    ax.legend(loc="lower right")


    plt.tight_layout()
    plt.savefig(
        OUTPUT_DIR / f"{name}_mollweide_map.png",
        dpi=200,
        bbox_inches="tight"
    )
    plt.show()
    plt.close(fig)
