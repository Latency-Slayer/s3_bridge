import os
from datetime import datetime

from botocore.exceptions import ClientError
from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)

s3 = boto3.client('s3')

@app.route('/s3/raw/upload', methods=['POST'])
def hello_world():
    if "file" not in request.files:
        return jsonify({'error': 'No file found'})

    file = request.files['file']
    motherboard_uuid = request.form['motherboard_uuid']
    legal_name = request.form['legal_name']
    registration_number = request.form['registration_number']

    filename, file_extension = os.path.splitext(file.filename)

    new_file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{motherboard_uuid}_{legal_name}_{registration_number}{file_extension}"

    new_file_name = new_file_name.replace(" ", "-")

    try:
        if file.filename == '':
            return jsonify({'error': 'No file found'})

        s3.upload_fileobj(file.stream, "latency-slayer-bucket-s3-raw", new_file_name)

        return jsonify("Success")
    except ClientError as e:
        return jsonify({'error': str(e)})



if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
