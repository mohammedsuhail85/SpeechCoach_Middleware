from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug import secure_filename
import os
import datetime
import requests

from werkzeug.exceptions import BadRequestKeyError


UPLOAD_FOLDER = '/home/suhail/Desktop/SpeechEmotionAnalyzer/uploaded_vid'
ALLOWED_EXTENTIONS = ['mp4']

app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

video_path = "uploaded_vid/test_vid.mp4"
extension_list = ("*.mp4", "*.flv")


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS


# @app.route('/audio/get', methods=['GET', 'POST'])
def get_emotion_predicted(audio_path):
    if request.method == 'POST':
        try:
            url_emotion = "http://127.0.0.1:5000/audio/getemotion"
            url_transcript = "http://127.0.0.1:6000/audio/process"

            # multipart = {'file': open("sample.wav", 'rb')}
            # multipart = {'file': ('sample.wav', open(audio_path, 'rb'), 'audio/x-wav', {'Expires': '0'})}
            multipart = {'file': ('sample.wav', open(audio_path, 'rb'), 'audio/x-wav', {'Expires': '0'})}

            print("Making Request")
            # response_1 = requests.post(url_transcript, files=multipart)
            response_2 = requests.post(url_emotion, files=multipart)

            # if response_1.status_code == 200 and response_2 == 200:
            #     return jsonify({
            #         # "Emotion_Analysis": response_2.content,
            #         "Transcript": response_1.content
            #     })
            return response_2.json()
        except Exception as ex:
            ex.with_traceback()
            return jsonify({
                "Error": "Something went wrong"
            })


@app.route('/video/save', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print('request created')
        try:
            f = request.files['file']

            filename = f.filename.rsplit('.', 1)[0]
            current_time = str(datetime.datetime.now())

            if f and allowed_file(f.filename):
                filename_new = secure_filename(
                    filename + '_' + current_time + ".mp4")
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename_new))

                video_path = ("uploaded_vid/" + filename_new)
                print(video_path)

                return jsonify({
                    "Message": "Video Saved",
                "Video_Filename": video_path})
            else:
                return jsonify({'Error': 'Unsupported file format. Supports only .mp4 format'}), 400
        except BadRequestKeyError:
            return jsonify({'Error': "Missing Video file, Required : form-data with .mp4 and "
                                     "key name 'file'"}), 400
        except Exception as ex:
            ex.with_traceback()
            return jsonify({'Error': "System Error"}), 409


if __name__ == '__main__':
    try:
        app.run(debug=True, port=7000)

    except Exception as e:
        e.with_traceback()
