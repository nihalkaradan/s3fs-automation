# COS Bucket creation script 
Use this script to create S3 buckets on IBM Cloud Object Storage

## Prerequisite -

```bash
pip install ibm-cos-sdk
```

## Creating S3 buckets on COS

1. Add/Remove bucket names from/to the buckets_subpath.json file. If you are adding new bucket names to the files, the name should follow below naming convention 
	- gen2-xxxx-\<bucket name\>
    - ["subpath1/","subpath2/"]

2. Update below properties in cos.properties file
    - [env] 
    - COS_ENDPOINT = 
    - COS_API_KEY_ID = 
    - COS_INSTANCE_CRN =
    - LOCATION = 
    - BUCKET_LIST = 
3. Run cosscript.py

```bash
python cosscript.py <env>
```
