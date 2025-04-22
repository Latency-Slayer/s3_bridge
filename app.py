from flask import Flask
import boto3
from flask import jsonify

app = Flask(__name__)

s3 = boto3.resource('s3')

@app.route('/store/s3/raw')
def hello_world():
    buckets = dict()

    for bucket in s3.buckets.all():
        buckets[bucket.name] = bucket

    return jsonify(buckets)

if __name__ == '__main__':
    app.run()
