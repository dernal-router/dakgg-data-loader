import json
import boto3
import datetime

client = boto3.client('dynamodb')

def main(event, context):

    try:
        return 'Success'
    except Exception as e:
        print(f'melvorhiscores-poststats Exception was caught : {str(e)}')
