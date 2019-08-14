import os
import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score

plt.style.use("bmh")



def kmeansClustering(X, k):
	kmeans = KMeans(n_clusters=k, random_state=0).fit(X)
	labels = kmeans.labels_

	distortion = kmeans.inertia_

	centers = np.array(kmeans.cluster_centers_)

	return labels, distortion, centers


def addLabel(data, labels):

	data.loc[:, "label"] = labels

	return data


def clustering(X):

	distortions = []

	for k in range(2, 15):

		print("Clustering using k: ", k)

		labels, distortion, centers = kmeansClustering(X, k)

		distortions.append(distortion)

		print("Inertia: ", distortion)

		#data = addLabel(data, labels)

	elbowPlot(distortions)

	#return data


def elbowPlot(distortions):
	k = np.arange(2, 15)

	plt.figure(figsize=(12, 10))
	plt.plot(k, distortions, marker='o')
	plt.xlabel('Number of clusters', fontsize="x-large")
	plt.ylabel('Inertia', fontsize="x-large")

	plt.savefig("plots/elbow_plot.png", dpi=300)
	#plt.show()


def silhouetteScore(X, labels, k, centers):
	silhouette_avg = silhouette_score(X, labels)
	print("Silhouette Score for Cluster=5: ", silhouette_avg)


def plotClusters(X, data, k, col1, col2):

	cols = ["sandybrown", "indianred", "lightgreen", "gold", "cornflowerblue"]

	markers = ["o", "v", "^", "<", ">"]

	#plt.figure(figsize=(12, 10))

	for j in range(0, k):
		plt.scatter(data.loc[data.label==j, col1].values, data.loc[data.label==j, col2].values, color=cols[j], alpha=0.5)

	plt.xlabel(col1.upper())
	plt.ylabel(col2.upper())

	#plt.show()

	plt.savefig("../plots/cluster-plots/"+col1+"_"+col2+".png", dpi=200)
	plt.close()


def plotData(data, col1, col2):
	plt.scatter(data[col1].values, data[col2].values)
	plt.xlabel(col1.upper())
	plt.ylabel(col2.upper())
	#plt.show()

	plt.savefig("../plots/"+col1+"_"+col2+".png", dpi=200)


def convertToDateTime(data):
	data[["inception_date", "latest_transaction_date"]] = data[["inception_date", "latest_transaction_date"]].apply(pd.to_datetime)

	return data


def addMonth(data, col, colname):
	data.loc[:, colname] = data[col].dt.month

	return data



if __name__ == "__main__":
	"""
		1. To plot data in 2D: plotData(data, "frequency", "engagement")
		2. To plot clusters: plotClusters(X, data, 5, "frequency", "engagement")
	"""
	
	results_file = "../data/rfe_with_attributes.csv"

	data = pd.read_csv(results_file, sep=",")
	data = data.set_index("userid")

	data = convertToDateTime(data)
	data = addMonth(data, "inception_date", "inception_month")

	print(data.head())





