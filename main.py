from flask import Flask, jsonify, request
from notesandquiz import generate_notes_and_quiz
from chatbot import ask_question
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './tvhacks-frontend/public/'
CORS(app)


@app.route('/', methods=['GET'])
def home():
    if (request.method == 'GET'):
        data = "hello world"
        return jsonify({'data': data})


@app.route('/get_info', methods=['GET'])
def disp():
    print(request.args)

    data = generate_notes_and_quiz(request.args.get("url"))
    print(data)
    return jsonify({'data': data})

@app.route("/upload", methods=["POST"])
def upload_image():
    file = request.files["image"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        process_image(file_path)
        return {"message": "Image uploaded successfully"}, 200
    else:
        return {"message": "Invalid file"}, 400

def process_image(file_path):
    # Invoke the Python script with the image file path as an argument
    from text_to_image import create_bullets_json
    from create_slides import main_create_slides
    from create_audio_from_slides import create_audio_json
    from create_audio import create_mp3_files
    from slideDrawer import main_slides_drawer
    
    create_bullets_json(file_path)
    main_create_slides()
    main_slides_drawer()
    create_audio_json()
    create_mp3_files()


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# @app.route('/get_info', methods=['GET'])
# def ask_bot(question):
#     print(request.args)
#
#     data = ask_question(question)
#     return jsonify({'data': data})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
