#!/bin/bash

blobs="blobs/blobs.csv"
downloaded_filename="downloaded.csv"

cat $filelink | while read LINE; do
	blob=$LINE

	python main.py $blob

	sudo mysql -u root iwant_db -e "LOAD DATA INFILE '$downloaded_filename' \
	INTO TABLE customers_december \
	FIELDS TERMINATED BY ',' \
	LINES TERMINATED BY '\n' \
	IGNORE 1 ROWS"

	result=$?

	if [ $result -ne 0 ]; then
		echo "ERROR!"
		
	rm $downloaded_filename
done


