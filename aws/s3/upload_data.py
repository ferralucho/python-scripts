
import boto3

s3 = boto3.resource('s3')

data = open('sample_data.csv', 'rb')
s3.Bucket('incoming-data-ht').put_object(Key='sample_data8.csv', Body=data)

print("uploading to S3 completed")
