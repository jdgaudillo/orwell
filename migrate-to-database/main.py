import io
import os
import time
import sys
import shutil
import csv
import pandas as pd

from download_from_blob import downloadSingleBlob


if __name__ == "__main__":
	file = "migrate-to-database/blobs/blobs.csv"

	account_name = "bigdatablobstorageprod"
	account_key = "csnLRfmJEQTUD/V7vkMMIic4yIIBPvtW1B2MBaPolk5ULJKAOp9BKjLWJzz+WiDdrBPYu+w1zrKEe5lofZhxAQ=="
	container = "events"

	downloaded_filename = "downloaded.csv"

	blob_name = sys.argv[1]

	downloadSingleBlob(account_name, account_key, container)

	drop = ["calid", "propertyid", "src	activity", "original_video_content_id", "video_content_id", "original_video_category_id", "video_category_id", 
			"number_used", "currency", "amount", "free_access_tag", "producttype", "productname", "partner", "mobiletype", "session_startdt_year",
			"session_startdt_month", "session_startdt_day", "verified", "sourcescript", "is_known", "app_version", "modifieddate"]


	data = pd.read_csv(downloaded_filename, sep=",")
	data = data.drop(drop, axis=1)

	print("Downloaded data: ", len(data))

	data.to_csv(downloaded_filename, index=False)