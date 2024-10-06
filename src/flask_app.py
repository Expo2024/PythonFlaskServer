from flask import Flask, request, jsonify
from flask_cors import CORS
from cloudinary import api
import cloudinary

cloudinary.config(
    cloud_name = "dsf5jskjk",
    api_key = "172248515715777",
    api_secret = "RiQZVf2iukLHdmdMnk8za5jWpkE",
    api_proxy = "https://proxy.server:3128"  # Asegúrate de usar el proxy correcto
)


import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
CORS(app)

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
    except cloudinary.exceptions.GeneralError as e:
        return jsonify({'error': 'Cloudinary error occurred: ' + str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred: ' + str(e)}), 500
if __name__ == '__main__':
    app.run(debug=False)