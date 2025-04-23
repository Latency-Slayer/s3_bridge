import os
from datetime import datetime

from botocore.exceptions import ClientError
from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')

@app.route('/s3/raw/upload')
def hello_world():
    if "file" not in request.files:
        return jsonify({'error': 'No file found'})

    file = request.files['file']
    motherboard_uuid = request.form['motherboard_uuid']

    filename, file_extension = os.path.splitext(file.filename)

    new_file_name = f"{datetime.now().strftime('%d/%m/%Y')}_{motherboard_uuid}{file_extension}"

    try:
        if file.filename == '':
            return jsonify({'error': 'No file found'})

        s3.upload_fileobj(file.stream, "latency-slayer-bucket-s3-raw", new_file_name)

        return jsonify("Success")
    except ClientError as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run()
