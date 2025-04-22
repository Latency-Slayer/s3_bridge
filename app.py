from flask import Flask
import dotenv

app = Flask(__name__)

@app.route('/store/s3/raw')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
