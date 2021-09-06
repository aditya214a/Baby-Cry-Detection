# import csv, pathlib, librosa
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import warnings
# warnings.filterwarnings('ignore')
# from tensorflow.keras.models import load_model 
# import pickle

class Predict:
    def __init__(self):
        # self.model = load_model('ff_nn_v_Ac88_Be.h5')
        # self.model.load_weights("ff_nn_v_Ac88_Be_weights.h5")
        # file = open("scaler_param.obj",'rb')
        # self.sc = pickle.load(file)
        pass

    def predict(self,name,window):
        # songname = name+'.wav'
        # y, sr = librosa.load(songname, mono=True, duration=5)        
        # mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        # header = 'filename '
        # for i in range(1, 41):
        #     header += f' mfcc{i}'
        # header = header.split()
        # to_append = f'{name}.wav '
        # for e in mfcc:
        #     to_append += f' {np.mean(e)}'
        # op=list(to_append.split())
        # op.pop(0)
        # Xnew = self.sc.transform([op])
        # ynew = self.model.predict_proba(Xnew)
        # print(ynew)
        # if ynew[0][0]>ynew[0][1]:
        #     y=0
        # else:
        #     y=1
        y=1 #
        window.cry_toggle(y)