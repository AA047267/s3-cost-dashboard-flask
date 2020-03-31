# s3-cost-dashboard-flask

A dashbaord on Flask framework to visualize S3 Bucket Name, Size, and Cost per month. Only execution of 'All Buckets' and 'DataManagement' Tab has implemented. To run: Clone the repo, cd into repo, and then execute 'python3 app.py'

Beforehand, data has to be inserted in the DB, for that execute get-s3-info.py python script after making necessary changes in the DB config. This file will insert/update first 10 fetched entries from AWS S3 (can be modified in the script itself). Once data is the available in the DB then application can be made to run.

In order to fetch specific buckets info based upon TEAM tag, run this script dm-bucket-insert-to-db.py It will search through all the buckets for a specific team tag and will insert the data (name, size, cost) into mentioned table in table.
