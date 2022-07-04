import json
import boto3
import requests
import csv
import cv2
import os

# Bucket
BUCKET_NAME = 'data-lake-local'  
PREFIX = 'data-lake-local/'
URL_S3 = 'http://172.17.0.1:4566' #equivale ao host docker
REGION = 'us-east-1'      
    



def upload_handler(event, context):
    caminho = "./img.csv"
    # Variaveis Globais
    pos=(10,100)
    opacity = 100
    with open(caminho, "r") as imgs:
        imgcsv = csv.reader(imgs, delimiter=",")
        for coluna in imgcsv:
            try:
                f = open('/tmp/'+str(coluna[0])+'.jpg','wb')
                response = requests.get(coluna[1])
                f.write(response.content)
                f.close()
            except:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Access-Control-Allow-Methods, Access-Control-Allow-Origin, Content-Type, Origin',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'POST, OPTIONS'
                    },
                    'body': json.dumps({
                        'message': "Error in reading CSV",
                        'code': 404
                    })
                }    
            
            s3 = boto3.client('s3', endpoint_url=URL_S3, region_name=REGION)
            with open('/tmp/'+str(coluna[0])+'.jpg', "rb") as f:
                s3.upload_fileobj(f,BUCKET_NAME,str(coluna[0])+'.jpg')    
                print("upload successful")
                
    return  {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Headers': 'Access-Control-Allow-Headers, Access-Control-Allow-Methods, Access-Control-Allow-Origin, Content-Type, Origin',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },
            'body': json.dumps({
                'message': "Your message has been sent successfully",
                'code': 200
            })
        }