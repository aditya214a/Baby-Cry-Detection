import PySimpleGUI as sg
import time, threading
import images_Base64 as images
global stop
from record import Record

# window = None
draw = None
cry_id = None
continous_detection = None
ids = []

def cry_toggle(cry=1):
    global cry_id
    print("cry_id : ",cry_id)
    # 0 = cry
    if cry == 1:
        if not cry_id == None:
            draw.DeleteFigure(cry_id)
            cry_id = None
    elif cry == 0:
        if cry_id == None:
            cry_id=draw.DrawImage(filename=r'images\images\cry_ui.png', location=(100,100))


def make_window():
    # global window
    global draw
    stop = False

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
                    element_padding=(0,0),)
                    # no_titlebar = True)
                    # auto_close_duration = 600)
    draw = window['Graph']
    window.cry_toggle = cry_toggle
    return window,draw

def progress_bar_update(window):
    print("progressing...")
    global ids
    print(ids)
    for id in ids:
        id=ids.pop()
        draw.DeleteFigure(id)
    for i in range(5):
        time.sleep(1)
        ids.append(draw.DrawImage(filename=r'images\images\progress_bar.png', location=(608+65*i,233)))
        if stop==True:
            break

def reset_all():
    stop = True
    continous_detection = False
    cry_toggle()
    for i in ids:
        draw.DeleteFigure(i)

def continous_detect(window,r):
    continous_detection = True
    print(stop,continous_detection)
    while stop==False and continous_detection == True:
        print("Continuous Recording iterating")
        r.record(window,lambda : stop)
        print("ids: ",ids)
        pbu = threading.Thread(target=progress_bar_update,args=(window,))
        pbu.start()

def main():
    global stop, progress_bar, continous_detection
    continous_detection = False
    stop = True
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
                    continous_detection = False
                    pbu = threading.Thread(target=progress_bar_update,args=(window,))
                    t1 = threading.Thread(target=r.record, args=(window,lambda : stop,))#, j))
                    t1.start()
                    pbu.start()
                elif 689<x<844:
                    print("Stop recording")
                    print("[LOG] Clicked Stop button!")
                    stop = True
                elif 844<x<950:
                    print("Playback")
                    stop = False
                    play_thread = threading.Thread(target=r.play,args=(lambda : stop,))
                    pbu = threading.Thread(target=progress_bar_update,args=(window,))
                    play_thread.start()
                    pbu.start()
            elif 560<y<632 and 636<x<896:
                print("continuous detection")
                stop = False
                continous_detection = True
                cd = threading.Thread(target=continous_detect, args=(window,r,))
                cd.start()
                pbu = threading.Thread(target=progress_bar_update,args=(window,))
                pbu.start()

            elif 0<y<71 and 905<x<1023:
                r.close()
                break
            elif 650<y<760 and 554<x<1018:
                reset_all()
        else:
            for key in values:
                print(key, ' = ',values[key])

if __name__ == '__main__':
    main()
    for thread in threading.enumerate(): 
        print(thread.name)
