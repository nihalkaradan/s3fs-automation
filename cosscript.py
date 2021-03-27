import ibm_boto3
import json
from ibm_botocore.client import Config, ClientError
import configparser
import re
import sys


#COS property file

config = configparser.RawConfigParser()
config.read('cos.properties')

# Constants for IBM COS values
COS_ENDPOINT = config.get(sys.argv[1],'COS_ENDPOINT') 
COS_API_KEY_ID = config.get(sys.argv[1],'COS_API_KEY_ID')
COS_INSTANCE_CRN = config.get(sys.argv[1],'COS_INSTANCE_CRN')
LOCATION = config.get(sys.argv[1],'LOCATION')
BUCKET_LIST = config.get(sys.argv[1],'BUCKET_LIST')

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    ibm_auth_endpoint="https://iam.bluemix.net/oidc/token",
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT   
)
cos2 = ibm_boto3.client("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)

def create_bucket(bucket_name):
    print("Creating new bucket: {0}".format(bucket_name))
    try:
        cos.Bucket(bucket_name).create(
            CreateBucketConfiguration={
                "LocationConstraint": LOCATION
            }
        )
        
        print("Bucket: {0} created!".format(bucket_name))
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
    except Exception as e:
        print("Unable to create bucket: {0}".format(e))

# bucket_list.json will contain json file with the list of buckets
def put_directories(bucket_name,dir_array):
    for x in dir_array:
        cos2.put_object(Bucket=bucket_name,Key=x)
        print("Folder: {0} created!".format(x))

with open(BUCKET_LIST) as f:
  data = json.load(f)

for bucket_name,sub_paths in data.items() :
    bucket_name = re.sub("xxxx",sys.argv[1],bucket_name)
    print('Creating bucket: {0}',bucket_name)
    create_bucket(bucket_name)
    default_sub_paths = ["Input/","Output/","Archive/"]
    if(sub_paths is not None):
        sub_paths = sub_paths + default_sub_paths
    put_directories(bucket_name,sub_paths)


