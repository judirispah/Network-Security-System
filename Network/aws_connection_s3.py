from Network.exception.exception import NetworkException 
from Network.logging.logger import logging
from Network.Constants import AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,REGION_NAME,MODEL_BUCKET_NAME
import os
import boto3


class S3_connection:
    def __init__(self):
        self.access_key_id = os.getenv('AWS_KEY_ID')
        self.secret_access_key = os.getenv('AWS_ACCESS_KEY')
        self.region_name = REGION_NAME
        self.bucket_name = MODEL_BUCKET_NAME


    def connect(self):
            #To connect to the high-level interface, you’ll follow a similar approach, but use resource():

           self.s3client_resource=boto3.resource('s3',
                                            aws_access_key_id=self.access_key_id,
                                            aws_secret_access_key=self.secret_access_key,
                                            region_name=self.region_name
                                            )
           

           self.s3client_client=boto3.client('s3',
                                            aws_access_key_id=self.access_key_id,
                                            aws_secret_access_key=self.secret_access_key,
                                            region_name=self.region_name
                                            )