import PySimpleGUI as sg
import time

import pyaudio, wave, threading
import csv, pathlib, librosa
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

from tensorflow.keras.models import load_model 
model = load_model('../ff_nn_v1_Ac85.h5')

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

global stop
stop = 0
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

window = None

def predict(name):
    global model
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
    ynew = model.predict_classes(Xnew)
    ynew = 1
    print(ynew)
    ynew = 'Crying sound is detected' if ynew==0 else 'No crying sound is detected'
    window['output'].update(value = ynew, visible = True)

def record(window):
    print("[LOG] Recording audio!")
    frames = []
    songname = "output"
    WAVE_OUTPUT_FILENAME = "output.wav"
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        if stop == 1:
            print("returning")
            break
    else:
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        print(songname)
        t2 = threading.Thread(target=predict, args=(songname,))
        t2.start()

def close():
    """Close all open streams/files"""
    global stream, p, wf
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

def make_window():
    global window
    sg.theme('Dark')
    sg.set_options(element_padding=(10, 10))

    layout = [[sg.Button('Start Recording', button_color=('white', 'black')),
            sg.Button('Stop', button_color=('gray50', 'black')),
            sg.Button('Clear', button_color=('white', '#9B0023'),key="Reset"),
            sg.Button('Continuous Detection', button_color=('black', 'springgreen4')),
            sg.Button('Exit', button_color=('white', '#00406B'))],
            [sg.ProgressBar(5, orientation='h', size=(71, 10), key='-PROGRESS BAR-')],
            [sg.Text(text="Predicting output...",key="output")],
            [sg.Output(size=(130,15), font='Courier 8', key = '_output_')]]

    window = sg.Window("Baby cry detection",
                    layout,
                    default_element_size=(12, 1),
                    text_justification='r',
                    auto_size_text=False,
                    auto_size_buttons=False,
                    grab_anywhere=True,
                    default_button_element_size=(20, 2))
                    # no_titlebar=True,
    return window


def progress_bar_update(window):
    for i in range(5):
        time.sleep(1)
        progress_bar.UpdateBar((i + 1))
        if stop==1:
            break

def continous_detection(window):
    while stop==0:
        record(window)
        pbu = threading.Thread(target=progress_bar_update,args=(window,))
        pbu.start()

def main():
    global stop, progress_bar
    window = make_window()
    progress_bar = window['-PROGRESS BAR-']
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
            close()
            break
        elif event == 'Start Recording':
            stop = 0
            pbu = threading.Thread(target=progress_bar_update,args=(window,))
            t1 = threading.Thread(target=record, args=(window,))#, j))
            t1.start()
            pbu.start()
        elif event == 'Stop':
            print("[LOG] Clicked Stop button!")
            stop = 1
        elif event == 'Continuous Detection':
            print("Continous detection has started")
            stop = 0
            cd = threading.Thread(target=continous_detection, args=(window,))
            cd.start()
            pbu = threading.Thread(target=progress_bar_update,args=(window,))
            pbu.start()
        elif event == 'Reset':
            window.FindElement('_output_').Update('')
        else:
            for key in values:
                print(key, ' = ',values[key])

if __name__ == '__main__':
    main()
    for thread in threading.enumerate(): 
        print(thread.name)