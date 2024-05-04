import boto3
import os
import logging
import time
from botocore.exceptions import ClientError

"""
This script uploads images to an Amazon S3 bucket using boto3. It imports necessary modules for OS interaction, error logging, and time control. 
The 's3_upload_image' function uploads a file to the S3 bucket, using the file name as the object name if none is provided. It logs and prints any errors that occur during the upload.
The 'main' function uploads all files in the 'Images' directory to the S3 bucket, pausing for 30 seconds between successful uploads.
If the script is run directly, it starts the upload process by calling the 'main()'.

"""

# Create an S3 client using boto3
s3_client = boto3.client('s3')

# Define a function to upload an image to an S3 bucket
def s3_upload_image(file_name, bucket='cpd-viracare-s3-bucket-s1935085', object_name=None):

    # If no object name is provided, use the file name as the object name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Try to upload the file to the S3 bucket
    try:
        # The file is in the 'Images' directory, so join the directory name with the file name
        s3_client.upload_file(os.path.join('Images', file_name), bucket, file_name)
        # If the upload is successful, print a success message
        print (f'The {file_name} was successfully uploaded to the S3 Bucket')
        # Return True to indicate success
        return True
    # If there's an error during the upload, handle it
    except ClientError as e:
        # Log the error
        logging.error(e)
        # Print an error message
        print(f'{file_name} experienced and error while uploading to the S3 Bucket: {e} )')
        # Return False to indicate failure
        return False

# Define the main function that will upload all images in the 'Images' directory
def main():
    # Get a list of all files in the 'Images' directory
    image_files = os.listdir('Images')

    # For each file in the directory, try to upload it to the S3 bucket
    for file_name in image_files:
        # Call the upload function and get the result
        success = s3_upload_image(file_name=file_name)
        # If the upload was successful, wait for 30 seconds before the next upload
        if success:
            time.sleep(30)

# If this script is run directly (not imported as a module), start the upload process
if __name__ == '__main__':
    main()
