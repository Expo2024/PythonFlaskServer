from flask import Flask, request, jsonify
from flask_cors import CORS
from cloudinary import api
import cloudinary
import cloudinary.uploader
from decouple import config

app = Flask(__name__)
CORS(app)

cloudinary.config(
    cloud_name = config("CLOUD_NAME"),
    api_key = config("CLOUD_API_KEY"),
    api_secret = config("CLOUD_API_SECRET")
)

@app.route('/')
def index():
    return "No deberias estar viendo esto"

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'nofile'}), 400
    
    file = request.files['file']

    try:
        response = cloudinary.uploader.upload(file,folder='uploads')

        return jsonify({'message': 'file uploaded','url': response['secure_url']}), 200
    
    except Exception as error:
        return jsonify({'error': error}), 500

@app.route('/images', methods=['GET'])
def get_images():
    try:
        response = api.resources(type='upload', prefix='uploads/')

        return jsonify({'message': 'images retrieved', "images": response['resources']}), 200
    except Exception as error:
        return jsonify({'error': error}), 500
if __name__ == '__main__':
    app.run(debug=True)
    
