from pydub import AudioSegment
from flask import Flask,request,jsonify,send_file
import requests,os
import json

import soundfile as sf
import speech_recognition as sr  # Initialize recognizer class

from flask_cors import CORS
app = Flask(__name__)
CORS(app)
import google.generativeai as genai

import os
api_key="AIzaSyC0O4dCvtLxrXg3BMBciSzrXhO3Vkb5Irw"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
convo = model.start_chat()

model = genai.GenerativeModel('gemini-1.5-flash')
convo = model.start_chat()
print(convo.send_message("SETTINGS PROMPT = changing your name to Venom and you have to start a conversation with the user like a real person, start a conversation with the person and go with the flow , the goal of this is to improve the communication of the user , give reply in one sentence, start the conversation with 'hey there, what's your name'").text)
UPLOAD_FOLDER = 'uploads/'
CONVERTED_FOLDER = 'converted/'
PlayhtGEN_FOLDER = 'PlayhtGEN/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)
os.makedirs(PlayhtGEN_FOLDER, exist_ok=True)

count=0

@app.route('/',methods=['GET','POST'])
def hello_world():
    # if request.method == 'POST':
    # global count
    # if count==0:
    #     first_text=convo.send_message(
    #         "changing your name to kunal and you have to start a conversation with the user like a real person, start a conversation with the person and go with the flow , the goal of this is to improve the communication of the user ").text
    #     count += 1
    #     return jsonify(first_text)

    if 'file' not in request.files:
        return 'No file part', 400

    file = request.files['file']

    if file.filename == '':
        return 'No selected file', 400

    if file:
        original_filename = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(original_filename)


    # Load the audio file
    audio = AudioSegment.from_file(os.path.join(UPLOAD_FOLDER, file.filename))

    # Export the audio file to a new format
    # Export the audio file to a new format
    audio.export(os.path.join(CONVERTED_FOLDER, 'output_file.wav'), format="wav")
    audio.export('output_file.wav', format="wav")
    print('output audio done')




    # methods starts from here

    recognized_text=speech_rec()
    gemini_RESP=gemini_reply(recognized_text)

    # file_loc=playht_audio(gemini_RESP)
    file_loc=gttsfunc(gemini_RESP)


    # reactresp={'file':file_loc}
    # return jsonify(reactresp)
    return send_file(path_or_file=file_loc,mimetype='audio/wav')



def speech_rec():
    r = sr.Recognizer()  # audio object
    audio = sr.AudioFile(os.path.join(CONVERTED_FOLDER, 'output_file.wav'))  # read audio object and transcribe
    with audio as source:
        audio = r.record(source)
        result = r.recognize_google(audio)

    print(result)
    return result

def restart():
        global convo
        convo=model.start_chat()
        return "DELETED"


def gemini_reply(recognized_text):
    if recognized_text=="DELETE HISTORY":
        return restart()
    return convo.send_message(recognized_text).text




# from pyht import Client, TTSOptions, Format

# client = Client("KZmMbhR2ViPU2WUdf1QsO4QATn32", "d1d9c18a9f97410ab5c4d5b64e8e4e85")

# options = TTSOptions(
#     # this voice id can be one of our prebuilt voices or your own voice clone id, refer to the`listVoices()` method for a list of supported voices.
#     voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json",
#     sample_rate=44_100,
#     format=Format.FORMAT_WAV,
#     speed=0.8,
# )

# def playht_audio(text):
#     # text = "Hey, this is kunal from Play. Please hold on a moment, let me just pull up your details real quick."
    

#     with open(os.path.join(PlayhtGEN_FOLDER, 'text_to_speech.wav'), "wb") as audio_file:
#         for chunk in client.tts(text=text, voice_engine="PlayHT2.0-turbo", options=options):
#             audio_file.write(chunk)
#     print("audio generated")
#     return os.path.join(PlayhtGEN_FOLDER, 'text_to_speech.wav')


from gtts import gTTS

def gttsfunc(text):
    myobj = gTTS(text=text, lang='en', slow=False)
    filename=os.path.join(PlayhtGEN_FOLDER, 'text_to_speech.wav')
    myobj.save(filename)
    return filename




@app.route('/generate',methods=['GET',"POST"])
def generateReport():
    PROMPT='Analyze the conversation history, correct and modify only the user response according to the grammer and IELTS exam preparation, and provide the analysis in the json format: [{"gemini":"reply","user":"response","correction":"if any"}],do not add any thing in the start and in the end of the format such as (```json), '
    response=gemini_reply(PROMPT)
    print(response)
    try:
     data=json.loads(response)
     return data
    except:
        return [] 


@app.route('/deleteHistory',methods=['GET','POST'])
def deleteHistory():
    response=gemini_reply(recognized_text="DELETE HISTORY")
    print(response)
    return response


if __name__ == '__main__':

    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
