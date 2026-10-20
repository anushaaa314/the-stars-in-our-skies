import requests
import pandas as pd
from io import StringIO

print("running... ")
url = "https://gea.esac.esa.int/tap-server/tap/sync"
query = """
SELECT TOP 20000
    source_id, 
    ra, 
    dec, 
    parallax, 
    phot_g_mean_mag,
    phot_bp_mean_mag,
    phot_rp_mean_mag,
    teff_gspphot,
    pmra, 
    pmdec, 
    classprob_dsc_combmod_star
FROM gaiadr3.gaia_source
WHERE random_index BETWEEN 0 AND 10000000
    AND parallax > 0 
    AND ra IS NOT NULL
    AND dec IS NOT NULL
    AND phot_g_mean_mag IS NOT NULL
    AND phot_bp_mean_mag IS NOT NULL 
    AND phot_rp_mean_mag IS NOT NULL
    AND teff_gspphot IS NOT NULL
    AND pmra IS NOT NULL
    AND pmdec IS NOT NULL
    AND (
        classprob_dsc_combmod_star >= 0.8
    )
    ORDER BY random_index
"""

response = requests.get(
    url,
    params={
        "REQUEST": "doQuery",
        "LANG": "ADQL",
        "FORMAT": "csv",
        "QUERY": query
    },
    timeout=300
)

print("Status code:", response.status_code)
print("Gaia's error message:")
print(response.text[:3000])

response.raise_for_status()

stars = pd.read_csv(StringIO(response.text))
stars.to_csv("stars.csv", index=False)

print(f"Total number of stars downloaded: {len(stars)}")
print(stars.head())