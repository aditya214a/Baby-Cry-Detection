import PySimpleGUI as sg
import time
import threading
from record import Record

from signal import signal, SIGINT
from sys import exit
def handler(signal_received, frame):
    stop_prediction = True
    print('\n\n\nAborting')
    exit(0)

signal(SIGINT, handler)

# Global variables
stop_prediction = False
r = Record()
while stop_prediction == False:
    # print("Continuous Recording iterating")
    r.record(lambda: stop_prediction)