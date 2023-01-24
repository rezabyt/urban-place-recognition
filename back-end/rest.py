from flask import Flask, request, render_template
import os
import json
from flask_cors import CORS
from werkzeug.utils import secure_filename
from responser import Responser

app = Flask(__name__)
CORS(app)

resp = Responser()


@app.route('/', methods=['GET'])
def index():
    return render_template('ا.html')


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['avatar']

        # Save the image to ./uploads
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, 'uploads', secure_filename(f.filename))
        f.save(image_path)

        # Make prediction
        predicted_classes = resp.get_predicted_classes(image_path)
        response = app.response_class(
            response=json.dumps(predicted_classes),
            mimetype='application/json'
        )

        return response
    return None


@app.route('/detail/<image_id>', methods=['GET'])
def detail(image_id):
    if request.method == 'GET':
        image_detail = resp.get_image_detail(image_id)

        response = app.response_class(
            response=json.dumps(image_detail),
            mimetype='application/json'
        )
        return response

    return None


@app.route('/gallery', methods=['GET'])
def gallery():
    if request.method == 'GET':
        gallery = resp.get_gallery()

        response = app.response_class(
            response=json.dumps(gallery),
            mimetype='application/json'
        )
        return response

    return None


if __name__ == '__main__':
    app.run()
