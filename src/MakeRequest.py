from flask import Flask, request, jsonify
import requests
from pydub import AudioSegment

FACE_URI="192.168.43.151"
GESTURE="192.168.43.62"
SPEECH_EMOTION=""
SPEECH_TRANSCRIPT=""


def start_face(session, file_path):
    try:
        face_url = "http://"+FACE_URI+":8000/FacialAnalysis/sessions/"+session+"/upload"

        file = {'file': open(file_path, 'rb')}
        response = requests.post(face_url, files=file)

        print(response)

        return response

    except Exception as ex:
        # ex.with_traceback()
        return jsonify({
            'Error': str(ex)
        }), 409


def start_voice_emotion(session, file_path):
    try:
        voice_emotion_url = "http://localhost:5000/audio/"+session+"/getemotion"
        print("session :" +session + " file: " + file_path)

        file = {'file': open(file_path, 'rb')}
        result = requests.post("http://localhost:5000/audio/"+session+"/getemotion", files=file)

        print(result)

        return result

    except Exception as ex:
        # ex.with_traceback()
        return jsonify({
            'Error': str(ex)
        }), 409


def start_transcript(session, file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        audio_name = file_path.split('.mp4')[0]
        audio_path = audio_name + ".wav"
        print(audio_path)
        audio.set_channels(1).set_frame_rate(16000).export(audio_path, format="wav")

        transcript_url = "http://localhost:6000/audio/"+session+"/process"
        file = {'file': open(audio_path, 'rb')}
        # multipart = {'file': ("file_audio", open(audio_path, 'rb'), 'audio/x-wav', {'Expires': '0'})}

        response = requests.post(transcript_url, files=file)

        print(response)

    except Exception as ex:
        # ex.with_traceback()
        return jsonify({
            'Error': str(ex)
        }), 409


def start_gesture(session, file_path):
    try:
        gesture_url="http://"+GESTURE+":4000/video/"+session+"/gesture"

        file = {'file': open(file_path, 'rb')}

        response = requests.post(gesture_url, files=file)

        print(response)

        return response

    except Exception as ex:
        # ex.with_traceback()
        return jsonify({
            'Error': str(ex)
        }), 409
