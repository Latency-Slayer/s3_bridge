from flask import Flask
import boto3

app = Flask(__name__)

s3 = boto3.resource('s3')

@app.route('/store/s3/raw')
def hello_world():
    for bucket in s3.buckets.all():
        print(bucket.name)


if __name__ == '__main__':
    app.run()
