import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

user_count, movie_count = 6040, 3952
data = np.zeros(shape=(user_count, movie_count), dtype=int)
with open("ratings.dat", "r") as f:
    for e in f.readlines():
        user_id, movie_id, rating, _ = map(int, e.split("::"))
        data[user_id - 1, movie_id - 1] = rating
data_df = pd.DataFrame(data)

pipe = make_pipeline(StandardScaler(), KMeans(n_clusters=3, n_init=10, random_state=0))
pipe.fit(data)
pred = pipe.predict(data)

au = lambda df: df.sum(axis=0)
avg = lambda df: df[df != 0].mean(axis=0)
sc = lambda df: (df != 0).sum(axis=0)
av = lambda df: (df >= 4).sum(axis=0)
bc = lambda df: (df[df != 0].rank(axis=1) - 1).sum(axis=0)
cr = lambda df: np.sign(df.apply(lambda col: np.sign(df.rsub(col, axis=0)).sum(axis=0))).sum(axis=0)
rs = lambda df, top=10: pd.DataFrame([(e(df).sort_values(ascending=False).index + 1)[:top] for e in (au, avg, sc, av, bc, cr)], index=pd.Index(("AU", "AVG", "SC", "AV", "BC", "CR"), name="method"), columns=pd.RangeIndex(1, top + 1, name="rank")).T

for i in range(3):
    print(f"group {i}")
    print(rs(data_df[pred == i]))
    print()

"""
group 0
method    AU   AVG    SC    AV    BC    CR
rank                                      
1        260  1164  1580  1198   260  1198
2       1198  2930  1270  1196  1198   260
3       1196   981  1196   260   593   858
4       1270  1741   589   593  1196  1196
5        593  1795   480   589   296   296
6        589  1420  2571  1270   858   593
7       2571   572  2716   858   608   318
8        296  1664   260  2762  2571   608
9        858  3800   457   318   589  2571
10      1240  3245  1210  1200  2762  2762

group 1
method    AU   AVG    SC    AV    BC    CR
rank                                      
1       1196   787  1196  1196   260   260
2        260  3881   260   260  1196  1198
3       1198  1360  1270  1198  1198  1196
4       2858  3866  1580  2858  2858  2858
5       2571   557  1210  2571  2571  2571
6        608  2765  2858   593   608   608
7       1270  1384  2571  2028   593   593
8        593  3012   480   608  2028   318
9       1210  2999  1265  1270   318   858
10      2028  2503  1198   318   858  1197

group 2
method    AU   AVG    SC    AV    BC    CR
rank                                      
1       2858  2962  2858  2858  2858  2858
2        260   578   260   260   260   260
3       1196  2198  1196  1196  1196  1196
4       1210  3233  1210  2028  2028  2028
5       2028  1830  2028   593  2571  1210
6        593  3656   480  2762  2762   593
7       2762  3245   589  1210   593  2762
8       2571  1787   593  1198   527   527
9        589  3607  2571  2571  1198  1198
10      1198   649  2762   527  1210  2571
"""
