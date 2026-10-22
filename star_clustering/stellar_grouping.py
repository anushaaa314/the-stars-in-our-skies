from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib as plt


stars = pd.read_csv("star_clustering/star_data.csv")
print(stars.head())