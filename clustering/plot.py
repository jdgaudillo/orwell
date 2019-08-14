import warnings
warnings.filterwarnings("ignore")

import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt 
import matplotlib.cm as cm
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_samples, silhouette_score
from matplotlib.colors import ListedColormap

plt.style.use("bmh")


def convertToDateTime(data):
	data[["inception_date", "latest_transaction_date"]] = data[["inception_date", "latest_transaction_date"]].apply(pd.to_datetime)

	return data


def peakDistribution(data, label, col):
	data = data.loc[data.label==label]

	data = convertToDateTime(data)

	hist, bins = np.histogram(data[col].values)
	labels = np.arange(1,11)
	data.loc[:, "bins"] = pd.cut(data[col], bins=bins, labels=labels)

	data = data.loc[data.bins.isin([1, 2])]

	hist, bins = np.histogram(data[col].values)
	data.loc[:, "peak_bins"] = pd.cut(data[col], bins=bins)

	print("Mode: ", data["peak_bins"].mode())

	distribution = data.groupby(["peak_bins"])["userid"].count()

	print(distribution)

	ax = distribution.plot.bar(rot=0, alpha=0.7, figsize=(12,10))

	ax.set_xlabel("RECENCY")
	ax.set_ylabel("CUSTOMERS")

	plt.savefig("../plots/cluster-plots/"+str(label)+"/peak_distribution"+col+".png", dpi=200)
	plt.close()


def getPeakDistribution(data, label, col):
	data = data.loc[data.label==label]

	data = convertToDateTime(data)

	data.loc[:, "inception_month"] = data.inception_date.dt.month

	#data = data.drop(data.loc[data.inception_month==5].index)

	# Make Recency Buckets
	hist, bins = np.histogram(data[col].values)
	labels = np.arange(1,11)
	data.loc[:, "bins"] = pd.cut(data[col], bins=bins, labels=labels)

	data = data.loc[data.bins==1]

	hist, bins = np.histogram(data[col].values)
	data.loc[:, "peak_bins"] = pd.cut(data[col], bins=bins)


	#print("MEDIAN: ",data["peak_bins"].median())
	print("Mode: ",data["peak_bins"].mode())

	distribution = data.groupby(["peak_bins", "inception_month"])["userid"].count().to_frame().reset_index()
	distribution.columns = ["peak_bins", "inception_month", "customers"]


	distribution = distribution.pivot(index="peak_bins", columns="inception_month", values="customers")
	distribution = distribution.fillna(0)
	#distribution.columns = ["January", "February", "March", "April", "May", "December"]

	print(distribution.columns)

	ax = distribution.loc[:, distribution.columns].plot.bar(stacked=True, rot=0, alpha=0.7)
	ax.set_xlabel("RECENCY")
	ax.set_ylabel("CUSTOMERS")

	distribution.to_csv("../data/data.csv")

	#plt.savefig("../plots/cluster-plots/"+str(label)+"/peak"+col+"_with_inception_withoutnewcustomers.png", dpi=200)
	#plt.close()

	#plt.show()



def distributionWithInception(data, label, col):
	data = data.loc[data.label==label]

	data = convertToDateTime(data)

	data.loc[:, "inception_month"] = data.inception_date.dt.month

	# Make Recency Buckets
	hist, bins = np.histogram(data[col].values)
	data.loc[:, "bins"] = pd.cut(data[col], bins=bins)

	distribution = data.groupby(["bins", "inception_month"])["userid"].count().to_frame().reset_index()
	distribution.columns = ["bins", "inception_month", "customers"]

	distribution = distribution.pivot(index="bins", columns="inception_month", values="customers")
	distribution = distribution.fillna(0)
	distribution.columns = ["January", "February", "March", "April", "May", "November", "December"]

	print(distribution)

	ax = distribution.loc[:, distribution.columns].plot.bar(stacked=True, rot=0, alpha=0.7, figsize=(12,10))
	ax.set_xlabel("RECENCY")
	ax.set_ylabel("CUSTOMERS")


	distribution.to_csv("../data/data.csv")

	#plt.savefig("../plots/cluster-plots/"+str(label)+"/"+col+"_with_inception.png", dpi=200)
	#plt.close()


def plotClusters(data, label, col1, col2):

	plt.scatter(data.loc[data.label==label, col1].values, data.loc[data.label==label, col2].values, alpha=0.5)

	plt.xlim((0, data[col1].max()))
	plt.ylim((0, data[col2].max()))

	plt.xlabel(col1.upper())
	plt.ylabel(col2.upper())

	#plt.show()

	#plt.savefig("../plots/cluster-plots/"+col1+"_"+col2+".png", dpi=200)
	#plt.close()