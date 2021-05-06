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
    name = ''
    for audio_path_file in tqdm(glob2.glob(pathname=path_file)):
        path_file_name = audio_path_file.split("\\")[1]
        if name != path_file_name:
            name = path_file_name
            print(name)
        
        # if not path.exists(path_file_name):
        #     os.mkdir(path_file_name)
        #     print(f'create folder {path_file_name}')

        # audio = AudioSegment.from_file(audio_path_file, format="wav")
        # audio = audio[start_time:end_time]
        # file_name = path_file_name + "\\" + audio_path_file.split('\\')[-1]
        # print(file_name)
        # audio.export(file_name, format="wav")
        # audio, sr = librosa.load(file_name, mono=True, sr=SR)
        # print(f'Cut {librosa.get_duration(y=audio, sr=sr)} in file {audio_path_file}')
        audio, sr = librosa.load(audio_path_file, mono=True, sr=SR)
        if librosa.get_duration(y=audio) < 10:
            print(audio_path_file.split("\\")[-1])

    print('End cut audio')

if __name__ == '__main__':
    cut_audio('./data/*/*.wav')