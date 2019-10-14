from flask import Flask, request, jsonify
from flask_restful import Api
from werkzeug import secure_filename
import os
import datetime
import requests
import threading

from werkzeug.exceptions import BadRequestKeyError
import MakeRequest
import warnings
warnings.filterwarnings('ignore')

UPLOAD_FOLDER = '/home/suhail/Desktop/SpeechCoach_Middleware/uploaded_vid'
# UPLOAD_FOLDER = os.environ["UPLOAD_FOLDER"] if "UPLOAD_FOLDER" in os.environ else "./uploaded_vid"
PORT = 7000
ALLOWED_EXTENTIONS = ['mp4', 'wav']

app = Flask(__name__)
api = Api(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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


@app.route('/api/v1/video/<session>/save', methods=['POST'])
def upload_file(session):
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

                video_path = (UPLOAD_FOLDER + "/" + filename_new)
                print(video_path)

                voice_emotion = threading.Thread(target=MakeRequest.start_voice_emotion, args=(session, video_path))
                voice_emotion.start()

                transcript = threading.Thread(target=MakeRequest.start_transcript, args=(session, video_path))
                transcript.start()

                face_analysis = threading.Thread(target=MakeRequest.start_face, args=(session, video_path))
                face_analysis.start()

                gesture = threading.Thread(target=MakeRequest.start_gesture, args=(session, video_path))
                gesture.start()

                return jsonify({
                    "Session Id": session,
                    "Status": "Video Saved and Process Started",
                })

            else:
                return jsonify({'Error': 'Unsupported file format. Supports only .mp4 format'}), 400
        except BadRequestKeyError:
            return jsonify({'Error': "Missing Video file, Required : form-data with .mp4 and "
                                     "key name 'file'"}), 400
        except Exception as ex:
            # ex.with_traceback()
            return jsonify({
                'Error': str(ex)
            }), 409


@app.route('/audio/test', methods=['GET', 'POST'])
def test_api():
    if request.method == 'GET':
        return jsonify({
            "Message": "Success"
        })


if __name__ == '__main__':
    try:
        app.run(debug=True, port=PORT,host="0.0.0.0")

    except Exception as e:
        e.with_traceback()
