import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

user_count, movie_count = 6040, 3952
data = np.zeros(shape=(user_count, movie_count), dtype=np.int64)
with open("ratings.dat", "r") as f:
    for e in f.readlines():
        user_id, movie_id, rating, _ = map(int, e.split("::"))
        data[user_id - 1, movie_id - 1] = rating
data_df = pd.DataFrame(data)

km = KMeans(n_clusters=3)
km.fit(data)
pred = km.predict(data)

au = lambda df: df.sum(axis=0)
avg = lambda df: df[df != 0].mean(axis=0)
sc = lambda df: (df != 0).sum(axis=0)
av = lambda df: (df >= 4).sum(axis=0)
bc = lambda df: (df[df != 0].rank(axis=1) - 1).sum(axis=0)
cr = lambda df: np.sign(df.apply(lambda col: np.sign(df.rsub(col, axis=0)).sum(axis=0))).sum(axis=0)
rs = lambda df, top=10: pd.DataFrame([e(df).sort_values(ascending=False).index[:top] + 1 for e in (au, avg, sc, av, bc, cr)], index=pd.Index(("AU", "AVG", "SC", "AV", "BC", "CR"), name="method"), columns=pd.RangeIndex(1, top + 1, name="rank")).T

for i in range(3):
    print(f"group {i}")
    print(rs(data_df[pred == i]))
    print()
