from flask import Flask
import boto3
import json

app = Flask(__name__)

s3 = boto3.resource('s3')

@app.route('/store/s3/raw')
def hello_world():
    buckets = dict()

    for bucket in s3.buckets.all():
        buckets[bucket.name] = bucket

    return json.dumps(buckets)

if __name__ == '__main__':
    app.run()
