import PySimpleGUI as sg
import time, threading
import images_Base64 as images
global stop
from record import Record

# window = None
# progress_bar = None
draw = None
cry_id = None
def make_window():
    # global window
    global draw
    stop = False
    # sg.ChangeLookAndFeel('Black')
    # sg.theme('Black')
    # sg.set_options(element_padding=(0, 0),background_color='#ececec')

    # layout = [[sg.Button(image_data=images.start_recording2, key='Start Recording',tooltip="Start Recording"),
    #         sg.Button(image_data=images.stop, key='Continuous Detection',tooltip="Continuous Detection"),
    #         sg.Button(image_data=images.play, key='play',tooltip="Play"),
    #         sg.Button(image_data=images.stop5, key='Stop',tooltip="Stop"),
    #         sg.Button(image_data=images.clear, key="Clear",tooltip="Clear"),
    #         sg.Button(image_data=images.exit, key='Exit',tooltip="Exit")],
    #         [sg.ProgressBar(5, orientation='h', size=(41, 10), key='-PROGRESS BAR-')],
    #         [sg.Text(text="Predicting..",key="output")],
    #         [sg.Output(size=(73,15), font='Courier 8', key = '_output_')]]

    # layout_left = [[sg.Image(r'images\original_images\cry.png')],
    #         [sg.Image(r'images\original_images\predicting.png')],
    #         [sg.Image(r'images\original_images\output.png')]]
    # layout_right = [[sg.Button(image_data=images.play, key='exit',tooltip="Play",target=(-1, 0))],
    #     [sg.Image(r'images\original_images\right.png')]]
    # layout = [[sg.Column(layout_left),sg.Column(layout_right)],]

    layout = [[sg.Graph(background_color='White', canvas_size=(1024, 768),
          graph_bottom_left=(0,768), key='Graph', pad=(0,0), enable_events=True,
          graph_top_right=(1024, 0))]]#, drag_submits=True)]]
    
    window = sg.Window("Baby cry detection",
                    layout,
                    default_element_size=(12, 1),
                    text_justification='r',
                    auto_size_text=False,
                    auto_size_buttons=False,
                    grab_anywhere=True,
                    default_button_element_size=(20, 2),
                    element_padding=(0,0))
                    # background_color='#ececec')
    # window.Finalize()
                    # no_titlebar=True,
    # event, values = window.read()
    draw = window['Graph']
    return window,draw


ids = []
def progress_bar_update(window):
    print("progressing...")
    global ids
    for i in range(5):
        time.sleep(1)

        ids.append(draw.DrawImage(filename=r'images\images\progress_bar.png', location=(608+65*i,233)))

        # if stop==True:
        #     break

# def continous_detection(window,r):
#     while stop==False:
#         r.record(window,lambda : stop)
#         pbu = threading.Thread(target=progress_bar_update,args=(window,))
#         pbu.start()

def cry_toggle(cry=1):
    global cry_id
    # o = cry
    if cry == 1:
        if not cry_id == None:
            draw.DeleteFigure(cry_id)
            cry_id = None
    elif cry == 0:
        if cry_id == None:
            cry_id=draw.DrawImage(filename=r'images\images\cry_ui.png', location=(100,100))

def main():
    global stop, progress_bar
    stop = False
    window,draw = make_window()
    print("record!!!")
    r = Record()
    eve = None
    window.read()
    id=draw.DrawImage(data=images.ML_Demo_UI_2, location=(0,0))
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
            r.close()
            break

        elif event == "Graph":
            x=values['Graph'][0]
            y=values['Graph'][1]
            if 389<y<513:
                if 583<x<689:
                    print("Recording")
                    stop = False
                    pbu = threading.Thread(target=progress_bar_update,args=(window,))
                    t1 = threading.Thread(target=r.record, args=(window,lambda : stop,))#, j))
                    t1.start()
                    pbu.start()
                elif 689<x<844:
                    print("Stop recording")
                elif 844<x<950:
                    print("Playback")
            elif 100<y<425 and 100<x<425:
                cry_toggle(cry=0)
            
            elif 0<y<71 and 905<x<1023:
                break

            # if eve == 'Start Recording':
            #     stop = False
            #     pbu = threading.Thread(target=progress_bar_update,args=(window,))
            #     # t1 = threading.Thread(target=r.record, args=(window,lambda : stop,))#, j))
            #     # t1.start()
            #     pbu.start()

            # elif eve == 'Stop':
            #     print("[LOG] Clicked Stop button!")
            #     stop = True

            # elif eve == 'Continuous Detection':
            #     print("Continous detection has started")
            #     stop = False
            #     cd = threading.Thread(target=continous_detection, args=(window,r,))
            #     cd.start()
            #     pbu = threading.Thread(target=progress_bar_update,args=(window,))
            #     pbu.start()

            # elif eve == 'Clear':
            #     window.FindElement('_output_').Update('')
            #     if stop==True:
            #         progress_bar.UpdateBar(0)

            # elif eve == 'play':
            #     stop = False
            #     play_thread = threading.Thread(target=r.play,args=(lambda : stop,))
            #     pbu = threading.Thread(target=progress_bar_update,args=(window,))
            #     play_thread.start()
            #     pbu.start()
            # eve = None

        else:
            for key in values:
                print(key, ' = ',values[key])

if __name__ == '__main__':
    main()
    for thread in threading.enumerate(): 
        print(thread.name)
