import PySimpleGUI as sg
import time, threading
import images_Base64 as images
global stop
stop = False

window = None
progress_bar = None
def make_window():
    global window
    sg.theme('Dark')
    sg.set_options(element_padding=(10, 10))

    # layout = [[sg.Button('Start Recording', button_color=('white', 'black')),
    #         sg.Button('Continuous Detection', button_color=('black', 'springgreen4')),
    #         sg.Button('PLay last recorded song', button_color=('black', 'springgreen4'), key="play"),
    #         sg.Button('Stop', button_color=('gray50', 'black')),
    #         sg.Button('Clear', button_color=('white', '#9B0023'),key="Clear"),
    #         sg.Button('Exit', button_color=('white', '#00406B'))],
    #         [sg.ProgressBar(5, orientation='h', size=(71, 10), key='-PROGRESS BAR-')],
    #         [sg.Text(text="Predicting..",key="output")],
    #         [sg.Output(size=(130,15), font='Courier 8', key = '_output_')]]
    layout = [[sg.Button(image_data=images.start_recording2, key='Start Recording',tooltip="Start Recording"),
            sg.Button(image_data=images.stop, key='Continuous Detection',tooltip="Continuous Detection"),
            sg.Button(image_data=images.play, key='play',tooltip="Play"),
            sg.Button(image_data=images.stop5, key='Stop',tooltip="Stop"),
            sg.Button(image_data=images.clear, key="Clear",tooltip="Clear"),
            sg.Button(image_data=images.exit, key='Exit',tooltip="Exit")],
            [sg.ProgressBar(5, orientation='h', size=(41, 10), key='-PROGRESS BAR-')],
            [sg.Text(text="Predicting..",key="output")],
            [sg.Output(size=(73,15), font='Courier 8', key = '_output_')]]

    window = sg.Window("Baby cry detection",
                    layout,
                    default_element_size=(12, 1),
                    text_justification='r',
                    auto_size_text=False,
                    auto_size_buttons=False,
                    grab_anywhere=True,
                    default_button_element_size=(20, 2))
    # window.Finalize()
                    # no_titlebar=True,
    # event, values = window.read()
    return window


def progress_bar_update(window):
    for i in range(5):
        time.sleep(1)
        progress_bar.UpdateBar((i + 1))
        if stop==True:
            break

def continous_detection(window,r):
    while stop==False:
        r.record(window,lambda : stop)
        pbu = threading.Thread(target=progress_bar_update,args=(window,))
        pbu.start()

def main():
    global stop, progress_bar
    window = make_window()
    print("record!!!")
    from record import Record
    r = Record()

    # window['output'].update(value = "Ready!", visible = True)

    progress_bar = window['-PROGRESS BAR-']
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            for key in values:
                print(key, ' = ',values[key])
            r.close()
            break

        elif event == 'Start Recording':
            stop = False
            pbu = threading.Thread(target=progress_bar_update,args=(window,))
            t1 = threading.Thread(target=r.record, args=(window,lambda : stop,))#, j))
            t1.start()
            pbu.start()

        elif event == 'Stop':
            print("[LOG] Clicked Stop button!")
            stop = True

        elif event == 'Continuous Detection':
            print("Continous detection has started")
            stop = False
            cd = threading.Thread(target=continous_detection, args=(window,r,))
            cd.start()
            pbu = threading.Thread(target=progress_bar_update,args=(window,))
            pbu.start()

        elif event == 'Clear':
            window.FindElement('_output_').Update('')
            if stop==True:
                progress_bar.UpdateBar(0)

        elif event == 'play':
            stop = False
            play_thread = threading.Thread(target=r.play,args=(lambda : stop,))
            pbu = threading.Thread(target=progress_bar_update,args=(window,))
            play_thread.start()
            pbu.start()

        else:
            for key in values:
                print(key, ' = ',values[key])

if __name__ == '__main__':
    main()
    for thread in threading.enumerate(): 
        print(thread.name)