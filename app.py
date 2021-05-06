from flask import Flask, request, jsonify, redirect, render_template
import pickle
import librosa
import numpy as np
import os
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'wav'}
bird_titles = ['cliswa', 'doccor', 'dowoo', 'dusfly', 'easblu', 'easmea', 'eucdov', 'eursta', 'evegro', 'foxspa']
bird_names = ['Én vách đá (cliff swallow)', 'Chim ruồi(Doctor Bird)', 'chim gõ kiến (downy woodpecker)',
              'Chim đớp ruồi (Dusky Flycatcher)', 'Chim xanh phía Đông (Eastern Bluebird)',
              'Chim đồng cỏ (Eastern Meadowlark)', 'Chim bồ câu (Eurasian Collared-Dove)',
              'Chim sáo đá (European Starling)', 'Chim chích chòe (Evening Grosbeak)', 'Chim sẻ cáo (Fox Sparrow)']

app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'upload'
app.config['JSON_AS_ASCII'] = False


def allowed_file(file_name):
    return '.' in file_name and file_name.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


def extract_features(file_name):
    try:
        audio, sr = librosa.load(file_name, mono=True, sr=44100, res_type='kaiser_fast')
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
        mfccs_scaled = np.mean(mfccs.T, axis=0)
    except Exception as e:
        return None

    return mfccs_scaled


@app.route('/')
def upload_file():
    return render_template('index.html', check=False)


@app.route('/', methods=['POST'])
def upload():
    file = request.files['file']
    file_upload = secure_filename(file.filename)
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400

    if file and allowed_file(file_name=file.filename):
        file.save(os.path.join(app.config['UPLOAD_PATH'], file_upload))
        file_path = 'upload/'+file.filename
        mfccs = extract_features(file_name=file_path)
        with open('svc_bird.pkl', 'rb') as f:
            model = pickle.load(f)
        result = model.predict([mfccs])
        f.close()
        return render_template('index.html', check=True, result=bird_titles[result[0]], name=bird_names[result[0]])


if __name__ == '__main__':
    app.run(debug=True)

