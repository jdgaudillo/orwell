#!/bin/bash

blobs="blobs/blobs.csv"
downloaded_filename="downloaded.csv"

cat $blobs | while read LINE; do
	blob=$LINE

	echo $blob

	echo "Executing python script!"

	python3.5 main.py $blob

	mysql -u iwant iwant_db -ppwd@33iwant -e "LOAD DATA INFILE '$downloaded_filename' \
	INTO TABLE customers_december \
	FIELDS TERMINATED BY ',' \
	LINES TERMINATED BY '\n' \
	IGNORE 1 ROWS"

	result=$?

	if [ $result -ne 0 ]; then
		echo "ERROR!"
	fi 

	break

		
	rm $downloaded_filename

done


