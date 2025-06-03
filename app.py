import os
from datetime import datetime

from botocore.exceptions import ClientError
from flask import Flask, jsonify, request
import boto3
import json

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

        s3.upload_fileobj(file.stream, "latency-raw", f"{registration_number}/{motherboard_uuid}/{datetime.now().strftime('%Y-%m-%d')}/component-data/{new_file_name}")

        return jsonify("Success")
    except ClientError as e:
        return jsonify({'error': str(e)})


@app.route('/s3/raw/process/upload', methods=['POST'])
def send_process_data():
    try:
        data = request.get_json()

        motherboard_uuid = data["motherboard_uuid"]
        registration_number = data["registration_number"]
        legal_name = data["legal_name"]


        if not data:
            return jsonify({'error': 'No JSON provided'}), 400

        new_file_name = f"{registration_number}/{motherboard_uuid}/{datetime.now().strftime('%Y-%m-%d')}/process-data/{datetime.now().strftime('%Y-%m-%d')}_{motherboard_uuid}_{legal_name}_{registration_number}.json"
        new_file_name = new_file_name.replace(" ", "-")

        json_bytes = json.dumps(data["process_json"], indent=4).encode('utf-8')

        s3.put_object(Bucket="latency-raw", Key=new_file_name, Body=json_bytes, ContentType='application/json')

        return jsonify({'message': 'JSON file uploaded successfully!'})

    except Exception as e:
        return jsonify({'error': f'Error sending JSON to bucket: {str(e)}'}), 500

@app.route('/s3/raw/connections/upload', methods=['POST'])
def send_connections_data():
    try:
        data = request.get_json()

        motherboard_uuid = data["motherboard_uuid"]
        registration_number = data["registration_number"]
        legal_name = data["legal_name"]

        if not data:
            return jsonify({'error': 'No JSON provided'}), 400

        new_file_name = f"{registration_number}/{motherboard_uuid}/{datetime.now().strftime('%Y-%m-%d')}/connections-data/{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}_{motherboard_uuid}_{legal_name}_{registration_number}.json"
        new_file_name = new_file_name.replace(" ", "-")

        json_bytes = json.dumps(data["connections_json"], indent=4).encode('utf-8')

        s3.put_object(Bucket="latency-raw", Key=new_file_name, Body=json_bytes, ContentType='application/json')

        return jsonify({'message': 'JSON file uploaded successfully!'})
    except Exception as e:
        print(e)
        return jsonify({'error': f'Error sending JSON to bucket: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
