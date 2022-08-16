import json
import boto3
import requests
from datetime import *
import urllib.parse

from requests_aws4auth import AWS4Auth

credentials = boto3.Session().get_credentials()
ES_HOST = 'https://search-photos-s2jfh5xpge7nleokbrq2kn4r5m.us-east-1.es.amazonaws.com/photos/_doc'
REGION = 'us-east-1a'



rekognition = boto3.client("rekognition", region_name = "us-east-1")

def lambda_handler(event, context):

    print("Adding code pipeline. Adding more add statements")
    print("Adding code pipeline. Adding more add statements")
    headers = { "Content-Type": "application/json" }    

    # TODO implement
    for record in event['Records']:
    # record = event['Records'][0]['s3']
        bucket = record['s3']['bucket']['name']
        photo = record['s3']['object']['key']
    
        res = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
            MaxLabels=10)
            
        # print(res)
        # print("The response is: ", res)
        obj = {}
        obj['objectKey'] = photo
        obj["bucket"] = bucket
        obj["createdTimestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        obj["labels"] = []
        
        for label in res['Labels']:
            obj["labels"].append(label['Name'].lower())
        
        
        print(obj)
        # url = get_url('photos')    
        req = requests.post(ES_HOST, json=obj, auth=("Cloud","Nobel@0399"))
        print(req.text)
    return {
        'statusCode': 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            'Content-Type': 'application/json'
        },
        'body': json.dumps("Image labels have been successfully detected!")
    }
