from pandas import * 

stars = read_csv("stars.csv")
print("original datset... ")
print(f"num of rows: {len(stars)}")
print(f"num of columns: {len(stars.columns)}")
print("missing values... ")
print(stars.isnull().sum())

before = len(stars)
stars = stars.drop_duplicates(subset="source_id")
print(f"duplicate rows removed: {before - len(stars)}")

before = len(stars)
stars = stars.dropna()
print(f"rows with missing column values removed: {before - len(stars)}")

before = len(stars)

stars = stars[
    stars["ra"].between(0, 360)
    & stars["dec"].between(-90, 90)
]
print(f"rows with invalid coordinates removed: {before - len(stars)}")

stars.to_csv("cleaned_stars.csv", index=False)
print(f"{len(stars)} cleaned rows saved to cleaned_stars.csv")

print("coordinate ranges: ")
print(stars[["ra", "dec"]].describe())