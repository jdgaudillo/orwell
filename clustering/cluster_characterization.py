import os
import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import seaborn as sns

from plot import distributionWithInception, getPeakDistribution, peakDistribution, plotClusters

plt.style.use("bmh")


def buildTable(data):
	cols = ["customers", "recency", "frequency", "engagement"]

	labels = data.label.unique()

	for i, label in enumerate(labels):
		print(label)
		tmp = data.loc[data.label==label]

		print("Customers: ", len(tmp))
		print("Recency: ", np.round(tmp.recency.mean(), 2))
		print("Frequency: ", np.round(tmp.frequency.mean(), 2))
		print("Engagement: ", np.round(tmp.engagement.mean(), 2))

		print("\n")


def attributeDistribution(data, col, label):

	data = data.loc[data.label==label]

	min_val = data[col].min()
	max_val = data[col].max()

	print(min_val, max_val)

	data[col].plot(kind="hist", figsize=(12,10))

	plt.xlabel(col.upper())
	plt.ylabel("CUSTOMERS")

	plt.xlim((min_val, max_val))

	plt.show()
	#plt.savefig("../plots/cluster-plots/"+str(label)+"/"+col+"_distribution.png", dpi=200)
	#plt.close()


if __name__ == "__main__":
	"""
		1. To build segment table: buildTable(data)
		2. To get distribution of attributes: attributeDistribution(data, "recency", 0)
		3. To get peak distribution: distributionWithInception(data, 0, "recency")
		4. To get peak distribution with inception month: getPeakDistribution(data, 0, "frequency")
	"""
	file = "../data/rfe_with_attributes.csv"

	data = pd.read_csv(file, sep=",")

	#plotClusters(data, 0, "recency", "engagement")





	

