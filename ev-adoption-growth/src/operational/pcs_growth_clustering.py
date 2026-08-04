# 5_pcs_growth_clustering.py

import pandas as pd
from sklearn.cluster import KMeans

df = pd.read_csv("data/OperationalPC.csv")

X = df[["No. of Operational PCS"]]

kmeans = KMeans(n_clusters=3, random_state=42)
df["Cluster"] = kmeans.fit_predict(X)

print("\n📊 Infrastructure Clusters:\n")
print(df[["State", "No. of Operational PCS", "Cluster"]])
