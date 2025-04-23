from flask import Flask, jsonify, request
import boto3

app = Flask(__name__)

s3 = boto3.resource('s3')

@app.route('/s3/raw/upload')
def hello_world():
    if "file" not in request.files:
        return jsonify({'error': 'No file found'})

    file = request.files['file']

    filename = "teste"

    if file.filename == '':
        return jsonify({'error': 'No file found'})

    s3.upload_fileobj(
        file,
        "latency-slayer-bucket-s3-raw",
        filename
    )


    return jsonify("Success")



if __name__ == '__main__':
    app.run()
