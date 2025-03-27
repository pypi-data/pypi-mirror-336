import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from rskpp.rskpp import rskmeanspp

# Generate synthetic dataset with 3 clusters
n_samples = 500
n_features = 2
n_clusters = 3

data, _ = make_blobs(n_samples=n_samples, centers=n_clusters, n_features=n_features, random_state=42)

# Apply rskpp function
k = n_clusters  # Number of clusters
m = 200  # Upper bound on rejection sampling iterations

centers = rskmeanspp(data, k, m)

# Apply KMeans using rskmeanspp centers as initialization
kmeans = KMeans(n_clusters=k, init=centers, n_init=1, random_state=42)
kmeans.fit(data)

# Plot dataset and final cluster centers
plt.scatter(data[:, 0], data[:, 1], s=10, label="Data points")
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], c='red', marker='x', s=100, label="Final centers")

plt.legend()
plt.title("K-Means with RS-k-means++ Initialization")
plt.savefig("cluster-plot.png")
plt.show()
