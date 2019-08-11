import warnings
warnings.filterwarnings("ignore")

import io
import os
import time
import shutil
import pandas as pd
import numpy as np

from zipfile import ZipFile
from azure.storage.blob import PublicAccess
from azure.storage.blob import BlockBlobService


def downloadBlob(account_name, account_key, container, downloaded_filename):
	block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

	print("Successfully accessed blob storage")

	generator = block_blob_service.list_blobs(container)

	for blob in generator: 
		print("Begin download")
		blob_arr = "{}".format(blob.name).split("/")
		
		year = blob_arr[1]
		month = blob_arr[2]
		blob_filename = blob_arr[3]

		print(month)

		if month != "11": break

		block_blob_service.get_blob_to_path(container, blob.name, downloaded_filename)

		print("Successfully downloaded ", downloaded_filename)
		print("\n")

		break


def downloadSingleBlob(account_name, account_key, container, blob_name):
	downloaded_file = "downloaded.csv"
	block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

	print("Downloading......")
	block_blob_service.get_blob_to_path(container, blob_name, downloaded_file)

	print("Successfully downloaded file: ", blob_name)


def getBlobNames(account_name, account_key, container):
	block_blob_service = BlockBlobService(account_name=account_name, account_key=account_key)

	print("Successfully accessed blob storage")

	generator = block_blob_service.list_blobs(container)

	blob_names = []

	for blob in generator: 
		blob_arr = "{}".format(blob.name).split("/")
		
		year = blob_arr[1]
		month = blob_arr[2]
		blob_filename = blob_arr[3]

		if month != "12": continue

		blob_names.append(blob.name)

	return blob_names


if __name__ == "__main__":
	"""
		1. To get list of blobs: getBlobNames(account_name, account_key, container)
	"""

	account_name = "bigdatablobstorageprod"
	account_key = "csnLRfmJEQTUD/V7vkMMIic4yIIBPvtW1B2MBaPolk5ULJKAOp9BKjLWJzz+WiDdrBPYu+w1zrKEe5lofZhxAQ=="
	container = "events"

	downloaded_filename = "downloaded.csv"
	