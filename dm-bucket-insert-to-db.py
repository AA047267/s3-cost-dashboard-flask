import mysql.connector
import os


# Config MySQL
hostname = 'localhost'
username = 'root'
password = 'QAZplm123!!!'
database = 's3_bucket'

cnx = mysql.connector.connect(user=username, password=password,
                              host=hostname,
                              database=database)

cursor = cnx.cursor()

buckets_name_list = []

out = os.popen("aws s3 ls | awk '{ print $3 }'").read()
buckets_name_list = list(out.split('\n'))

datamanagement_buckets = []

for bucket in buckets_name_list:
    try:
        tag = os.popen("aws s3api get-bucket-tagging --bucket "+bucket+"| jq -c '.[][] ' | grep TEAM | jq -r .Value | tr -d '[:space:]'").read()
        print(bucket)
        if tag == 'DATAMANAGEMENT':
            datamanagement_buckets.append(bucket)
    except:
        pass


print(datamanagement_buckets)

for bucket in datamanagement_buckets:
	try:
		print(bucket)
		size = float(os.popen("aws s3 ls s3://"+bucket+"/ --recursive | awk 'BEGIN {total=0}{total+=$3}END{print total/1024/1024/1024}'").read())
		float_cost = size * 0.023
		print(size)
		cost = float("%.2f" % float_cost)
		cursor.execute("INSERT INTO dm_bucket_size(name,size,cost) VALUES (%s, %s, %s)", (bucket, size, cost))
		cnx.commit()
	except:
		cursor.execute("UPDATE dm_bucket_size SET size = %s, cost = %s WHERE name = %s", (size, cost, bucket))
		cnx.commit()

print('Data has been written to DB - Success')
