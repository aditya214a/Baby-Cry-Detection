import ctypes
import platform
import threading
from io import BytesIO
from time import sleep

from PIL import Image
import PySimpleGUI as sg

def image_to_data(im):
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

def process_thread():
    global index
    while True:
        sleep(0.01)
        index = (index + 1) % frames
        window.write_event_value('Animation', index)

if platform.system() == "Windows":
    if platform.release() == "7":
        ctypes.windll.user32.SetProcessDPIAware()
    elif platform.release() == "8" or platform.release() == "10":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

im = Image.open("D:/1.gif")
width, height = im.size
frames = im.n_frames

graph_width, graph_height = size = (640, 640)

layout = [[sg.Graph(size, (0, 0), size, background_color='green', key='GRAPH')]]
window = sg.Window("Animation", layout, return_keyboard_events=True, finalize=True)

graph = window['GRAPH']
index = 0
im.seek(index)
data = image_to_data(im)
x, y = location = (graph_width//2-width//2, height)
item = graph.draw_image(data=data, location=location)

step = 20

thread = threading.Thread(target=process_thread, daemon=True)
thread.start()

while True:

    event, values = window.read(timeout=50)

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Animation':
        im.seek(index)
        data = image_to_data(im)
        item_new = graph.draw_image(data=data, location=location)
        graph.delete_figure(item)
        item = item_new
    elif event == "Left:37":
        x = x - step if x >= step else x
        location = (x, y)
    elif event == "Right:39":
        x = x + step if x <= graph_width - width - step else x
        location = (x, y)
    elif event == "Up:38":
        y = y + step if y <= graph_height - step else y
        location = (x, y)
    elif event == "Down:40":
        y = y - step if y >= height + step else y
        location = (x, y)

window.close()