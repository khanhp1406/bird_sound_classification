import os
import glob2
import librosa
import shutil
from os import path
from pydub import AudioSegment
from tqdm import tqdm


def cut_audio(path_file):

    start_time = 0
    end_time = 10 * 1000
    SR = 44100

    print('Start cut audio...')
    for audio_path_file in tqdm(glob2.glob(pathname=path_file)):
        print(path_file)
        path_file_name = path_file.split('\\')[1]

        if path.exists(path_file_name):
            continue
        else:
            os.mkdir(path_file_name)

        try:
            audio = AudioSegment.from_file(audio_path_file, format="wav")
            audio = audio[start_time:end_time]
            file_name = path_file_name + audio_path_file
            audio.export(file_name, format="wav")
            audio, sr = librosa.load(file_name, mono=True, sr=SR)
            print(f'Cut {librosa.get_duration(y=audio, sr=SR)} in file {audio_path_file}')
        except Exception:
            print('Duration audio < 10s')
            shutil.move(audio_path_file, path_file_name + audio_path_file)

    print('End cut audio')

if __name__ == '__main__':
    cut_audio('./data/*/*.wav')