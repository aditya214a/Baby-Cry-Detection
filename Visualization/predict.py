import csv, pathlib, librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.models import load_model 

class Predict:
    def __init__(self):
        self.model = load_model('../ff_nn_v1_Ac85.h5')

    def predict(self,name):
        # global model
        #Doing prediction
        cmap = plt.get_cmap('inferno')
        plt.figure(figsize=(8,8))
        pathlib.Path(f'live_data/').mkdir(parents=True, exist_ok=True)
        # for filename in os.listdir(f'b_cry/{g}'):
        songname = name+'.wav'
        y, sr = librosa.load(songname, mono=True, duration=7)
        plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB');
        plt.axis('off');
        plt.savefig(f'live_data/{name}.png')
        plt.clf()

        header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
        for i in range(1, 21):
            header += f' mfcc{i}'
        header += ' label'
        header = header.split()

        file = open(f'{name}.csv', 'w', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(header)
        y, sr = librosa.load(songname, mono=True, duration=5)
        rmse = librosa.feature.rms(y=y)
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        mfcc = librosa.feature.mfcc(y=y, sr=sr)
        to_append = f'{name}.wav {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'   
        for e in mfcc:
            to_append += f' {np.mean(e)}'
        file = open(f'{name}.csv', 'a', newline='')
        with file:
            writer = csv.writer(file)
            writer.writerow(to_append.split())
        live_data = pd.read_csv(f'{name}.csv')
        live_data = live_data.drop(['filename'],axis=1)
        Xnew = np.array([live_data.iloc[0][0:26]])
        ynew = self.model.predict_classes(Xnew)
        ynew = 1
        print(ynew)
        ynew = 'Crying sound is detected' if ynew==0 else 'No crying sound is detected'
        window['output'].update(value = ynew, visible = True)
