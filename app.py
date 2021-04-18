from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

import speech_recognition as sr
import pandas as pd

from gpt3 import prompt, parse_response
from icd_code_scraping import get_icd_codes

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 128 * 1024 * 1024

app.jinja_env.lstrip_blocks = True
app.jinja_env.trim_blocks = True


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.method)
    print(request.form)
    print(request.files)
    if request.method == 'GET':
        return render_template('main.html')
    if request.method == 'POST':
        text = ''
        if 'text' in request.form:
            text = request.form['text']
            print(text)
        elif 'audio_data' in request.files:
            file = request.files['audio_data']
            with open('audio.wav', 'wb') as audio:
                file.save(audio)
            r = sr.Recognizer()
            with sr.AudioFile('audio.wav') as source:
                audio_data = r.record(source)
                text = r.recognize_google(audio_data)
                print(text)
        response = prompt(text)
        print(response)
        response = parse_response(response)
        print(response)
        icd_codes = []
        for symptom in response['Symptoms:']:
            icd_results = get_icd_codes(symptom)
            for k, v in icd_results.items():
                icd_codes.append((symptom, k, v))
        print(icd_codes)
        pd.DataFrame.from_dict(response, orient='index').transpose().to_csv('dataframe.csv')
        return render_template('main.html', text=text, ai_response=response, icd_codes=icd_codes, request='POST')


@app.route('/dataframe')
def dataframe():
    return send_file('dataframe.csv')


if __name__ == '__main__':
    app.run()
