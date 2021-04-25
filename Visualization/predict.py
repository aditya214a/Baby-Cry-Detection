# import csv, pathlib, librosa
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('ignore')
# from tensorflow.keras.models import load_model 

class Predict:
    def __init__(self):
        pass
        # self.model = load_model('ff_nn_v1_Ac85.h5')

    def predict(self,name,window):
        # # global model
        # #Doing prediction
        # songname = name+'.wav'
        # # for filename in os.listdir(f'b_cry/{g}'):
        # # plt.figure(figsize=(8,8))
        # # cmap = plt.get_cmap('inferno')
        # # pathlib.Path(f'live_data/').mkdir(parents=True, exist_ok=True)
        # # y, sr = librosa.load(songname, mono=True, duration=7)
        # # plt.specgram(y, NFFT=2048, Fs=2, Fc=0, noverlap=128, cmap=cmap, sides='default', mode='default', scale='dB');
        # # plt.axis('off');
        # # plt.savefig(f'live_data/{name}.png')
        # # plt.clf()


        # y, sr = librosa.load(songname, mono=True, duration=5)
        # rmse = librosa.feature.rms(y=y)
        # chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        # spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        # spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        # rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        # zcr = librosa.feature.zero_crossing_rate(y)
        # mfcc = librosa.feature.mfcc(y=y, sr=sr)

        # header = 'filename chroma_stft rmse spectral_centroid spectral_bandwidth rolloff zero_crossing_rate'
        # for i in range(1, 21):
        #     header += f' mfcc{i}'
        # # header += ' label'
        # header = header.split()
        # # file = open(f'{name}.csv', 'w', newline='')
        # # with file:
        # #     writer = csv.writer(file)
        # #     writer.writerow(header)

        # to_append = f'{name}.wav {np.mean(chroma_stft)} {np.mean(rmse)} {np.mean(spec_cent)} {np.mean(spec_bw)} {np.mean(rolloff)} {np.mean(zcr)}'   
        # for e in mfcc:
        #     to_append += f' {np.mean(e)}'
        # # file = open(f'{name}.csv', 'a', newline='')
        # # with file:
        # #     writer = csv.writer(file)
        # #     writer.writerow(to_append.split())
        # to_append = to_append.split(' ')
        # # to_append = [[float(i) for i in to_append]]
        # to_append = [[to_append[0]]+[float(i) for i in to_append[1:]]]
        # live_data = pd.DataFrame(to_append,columns=header)
        # # live_data = pd.read_csv(f'{name}.csv')
        # live_data = live_data.drop(['filename'],axis=1)
        # Xnew = np.array([live_data.iloc[0][0:26]])
        # ynew = self.model.predict_classes(Xnew)
        ynew = 1
        print(ynew)
        ynew = 'The prediction: Crying sound is detected' if ynew==0 else 'The prediction: No crying sound is detected'
        window['output'].update(value = ynew, visible = True)
    
    def close(self):
        pass
