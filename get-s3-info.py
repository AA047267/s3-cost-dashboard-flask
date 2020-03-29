import mysql.connector
import os


# Config MySQL
hostname = 'localhost'
username = 'root'
password = '<DB Password - Replace>'
database = 's3_bucket'

cnx = mysql.connector.connect(user=username, password=password,
                              host=hostname,
                              database=database)

cursor = cnx.cursor()

buckets_name_list = []

out = os.popen("aws s3 ls | awk '{ print $3 }'").read()
buckets_name_list = list(out.split('\n'))   #Convert the output of bucket names to list





for bucket in range(0,10):  #Looping over first 10 bucket only. 
   try:
      size = float(os.popen("aws s3 ls s3://"+buckets_name_list[bucket]+"/ --recursive | awk 'BEGIN {total=0}{total+=$3}END{print total/1024/1024/1024}'").read()) #Getting the size in GB
      float_cost = size * 0.023
      cost = float("%.2f" % float_cost)  #Restricting only 2 values after decimal place
      cursor.execute("INSERT INTO s3_bucket_size(name,size,cost) VALUES (%s, %s, %s)", (buckets_name_list[bucket], size, cost))
      cnx.commit()
   except:
      cursor.execute("UPDATE s3_bucket_size SET size = %s, cost = %s WHERE name = %s", (size, cost, buckets_name_list[bucket]))
      cnx.commit()

#Try Except block is implemeneted to overwrite bucket info if exists or insert new entry if bucket doesn't exist in table.

print('Data has been written to DB - Success')




