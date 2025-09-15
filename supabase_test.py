# supabase_test.py

import boto3
from botocore.exceptions import ClientError
import os

# --- Your Exact Supabase Credentials ---
# Make sure these match your settings.py file
AWS_ACCESS_KEY_ID = '6f7ec20f2576810b0254b58655f43793'
AWS_SECRET_ACCESS_KEY = 'd8a030ef174bdfb352182f5e5b784261c51b1f705baf8888e3e7434c83894871' 
AWS_S3_ENDPOINT_URL = 'https://wpfindxipzpmtpvppneg.storage.supabase.co/storage/v1/s3'
AWS_S3_REGION_NAME = 'eu-west-1'
AWS_STORAGE_BUCKET_NAME = 'portfolio_media'

# --- Test File Details ---
file_name = 'local_test_file.txt'
bucket_key = 'direct_boto3_test/test_upload.txt' # The path inside the bucket

def create_test_file():
    """Creates a dummy file to upload."""
    print(f"1. Creating a local dummy file named '{file_name}'...")
    with open(file_name, "w") as f:
        f.write("This is a direct test of boto3 to Supabase.")
    print("   - Done.")

def upload_to_supabase():
    """Connects to Supabase and attempts to upload the file."""
    print("\n2. Attempting to connect to Supabase...")
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            endpoint_url=AWS_S3_ENDPOINT_URL,
            region_name=AWS_S3_REGION_NAME
        )
        print("   - Connection client created.")

        print(f"\n3. Uploading '{file_name}' to bucket '{AWS_STORAGE_BUCKET_NAME}'...")
        s3_client.upload_file(
            file_name,
            AWS_STORAGE_BUCKET_NAME,
            bucket_key,
            ExtraArgs={'ACL': 'public-read'} # This makes the file public
        )
        print("\n✅ SUCCESS! File uploaded to Supabase.")

        # Construct the public URL
        public_url = f"https://{AWS_STORAGE_BUCKET_NAME}.{AWS_S3_ENDPOINT_URL.replace('https://', '')}/{bucket_key}"
        # A more direct URL for supabase
        supabase_url = f"https://wpfindxipzpmtpvppneg.supabase.co/storage/v1/object/public/{AWS_STORAGE_BUCKET_NAME}/{bucket_key}"

        print(f"   - Public URL: {supabase_url}")

    except ClientError as e:
        print("\n❌ FAILED! A client error occurred.")
        print("   This is the real error message from Supabase/boto3:")
        print(f"   - Error Code: {e.response['Error']['Code']}")
        print(f"   - Error Message: {e.response['Error']['Message']}")
    except Exception as e:
        print(f"\n❌ FAILED! A general error occurred: {e}")
    finally:
        # Clean up the local file
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"\n4. Cleaned up local file '{file_name}'.")

if __name__ == "__main__":
    create_test_file()
    upload_to_supabase()
