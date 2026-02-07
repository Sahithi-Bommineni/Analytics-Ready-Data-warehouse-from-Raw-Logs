import boto3
import gzip
import io
import os
from tqdm import tqdm 



def upload_with_compression(local_file, bucket, s3_key,access_key, secret_key):
    s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name='us-east-1') #initialize s3
    file_size = os.path.getsize(local_file) #get the size of the file for progress bar 
    print(f"Starting ingestion: {local_file} -> s3://{bucket}/{s3_key}")
    try:
        with open(local_file, 'rb') as f_in:
            gz_buffer = io.BytesIO() #create a buffer to hold the compressed data
            with gzip.GzipFile(fileobj=gz_buffer, mode='wb') as gz:
                with tqdm(total=file_size, unit='B', unit_scale=True, desc=f"Compressing {local_file}") as pbar:
                    while True:
                        chunk = f_in.read(10 * 1024 * 1024) #read in 10MB chunks
                        if not chunk:
                            break
                        gz.write(chunk) #write the chunk to the gzip file
                        pbar.update(len(chunk)) #update the progress bar
            gz_buffer.seek(0) #reset the buffer position to the beginningcom
            compressed_size = gz_buffer.getbuffer().nbytes #get the size of the compressed data
            print(f"Compression complete: {compressed_size} bytes")
            with tqdm(total=compressed_size, unit='B', unit_scale=True, desc=f"Uploading {local_file} to S3") as pbar:
                s3.upload_fileobj(gz_buffer, bucket, s3_key, Callback=lambda bytes_transferred: pbar.update(bytes_transferred), ExtraArgs = {'ContentEncoding': 'gzip','ContentType': 'application/gzip'}) #upload the compressed data to S3 with a progress callback
                print(f"Upload complete: s3://{bucket}/{s3_key}")
    except Exception as e:
        print(f"Error during ingestion: {e}")

if __name__ == "__main__":
    #configuring variables for the ingestion
    local_file = "/Users/sahithi/Downloads/Yelp JSON/yelp_dataset/yelp_academic_dataset_business.json" #path to the local file
    bucket = "yelp-raw-data-sahithi" #name of the S3 bucket
    s3_destination_key = "raw/business.json.gz" #key for the file in S3 (including .gz extension)
    AWS_ACCESS = os.getenv("AWS_ACCESS_KEY") #get AWS access key from environment variable
    AWS_SECRET = os.getenv("AWS_SECRET_ACCESS_KEY") #get AWS secret key from environment variable
    upload_with_compression(local_file, bucket, s3_destination_key, AWS_ACCESS, AWS_SECRET) #call the function to upload the file with compression