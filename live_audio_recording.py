import pyaudio
import wave
import threading
import time

# t1 = threading.Thread(target=print_square, args=(10,))
# t2 = threading.Thread(target=print_cube, args=(10,))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

stop = 0
# p = pyaudio.PyAudio()

# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)

print("* recording")


def predict():
    for i in range(0,3):
        print(str(i*2))
        time.sleep(0.5)

# def record_audio():
for j in range(0,4):
# stop = 0
# file_name_itr = 0 # up till 3
# while(stop == 0):
#     frames = []
#     WAVE_OUTPUT_FILENAME = "output"+str(file_name_itr)+".wav"
#     for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#         data = stream.read(CHUNK)
#         frames.append(data)

#     wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
    print("START")
    for i in range(0,5):
        print(str(i*100))
        time.sleep(0.5)
    t2 = threading.Thread(target=predict, args=())
    t2.start()
    
# if __name__ == "__main__":
    # creating thread
# t1 = threading.Thread(target=record_audio, args=())
# t2 = threading.Thread(target=predict, args=())

# while(stop==0):
# t1.start()
# t2.start()
# t1.join()
# t2.join()
# both threads completely executed
print("Done!")