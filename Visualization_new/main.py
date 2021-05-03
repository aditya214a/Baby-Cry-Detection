import PySimpleGUI as sg
import time
import threading
import images_Base64 as images
from record import Record

# Global variables
window = None
draw = None
cry_ids = [None, None]  # No Cry, Cry
continous_detection = None
stop = False
pred_text_id = None


def predicting_ring_animation(draw):
    global stop
    frames = [('0.png', 2), ('2.png', 9), ('11.png', 4), ('15.png', 6),
              ('21.png', 4), ('25.png', 6), ('31.png',
                                             4), ('35.png', 7), ('42.png', 3),
              ('45.png', 6), ('51.png', 4), ('55.png',
                                             6), ('61.png', 4), ('65.png', 7),
              ('72.png', 3), ('75.png', 6), ('81.png', 4), ('85.png', 10), ]
    while True:
        for i in frames:
            predicting_ring_id = draw.DrawImage(
                filename="images\\UI_V2_1080p\\predicting_ring\\"+str(i[0]), location=(1283, 114))
            time.sleep(0.02*i[1])
            draw.DeleteFigure(predicting_ring_id)
        if stop == True:
            break


def cry_toggle(cry=None):
    """
        Display the picture on the left side of the screen for the predicted result.
    """
    # 0 = cry
    for i in cry_ids:
        draw.DeleteFigure(i)
    if cry == 1:
        cry_ids[1] = draw.DrawImage(
            filename=r'images\UI_V2_1080p\calm_ui.png', location=(260, 260))
    elif cry == 0:
        cry_ids[0] = draw.DrawImage(
            filename=r'images\UI_V2_1080p\cry_ui.png', location=(260, 260))


def predicting(pred=True, cont_detec=False):
    global pred_text_id, continous_detection,stop
    stop = not pred
    continous_detection = (cont_detec and pred)
    print("F=predicting: continous_detection: ", continous_detection)
    if pred_text_id == None and stop == False:
        pred_text_id = draw.DrawImage(
            filename=r'images\UI_V2_1080p\predicting.png', location=(1360, 250))
    elif not pred_text_id == None and stop == True:
        draw.DeleteFigure(pred_text_id)
        pred_text_id = None


def make_window():
    global draw, stop, cry_ids, window, continous_detection

    layout = [[sg.Graph(background_color='White', canvas_size=(1920, 1080),
                        graph_bottom_left=(0, 1080), key='Graph', pad=(0, 0), enable_events=True,
                        graph_top_right=(1920, 0))]]  # , drag_submits=True)]]

    window = sg.Window("Baby cry detection",
                       layout,
                       default_element_size=(12, 1),
                       text_justification='r',
                       auto_size_text=False,
                       auto_size_buttons=False,
                       default_button_element_size=(20, 2),
                       # grab_anywhere=True,
                       #    no_titlebar = True,
                       # auto_close_duration = 600,
                       margins=(0, 0),
                       element_padding=(0, 0),).Finalize()
    draw = window['Graph']
    id = draw.DrawImage(
        filename=r'images\UI_V2_1080p\Waiting.png', location=(0, 0))
    # arc_id = draw.draw_arc(top_left=(1283,114),
    #             bottom_right=(1596,427),
    #             extent=90,
    #             start_angle=0,
    #             style = 'last',
    #             arc_color = "blue",
    #             line_width = 15,
    #             fill_color = 'green')
    window.Maximize()
    window.bind("<Escape>", "-ESCAPE-")
    window.Finalize()

    window.cry_toggle = cry_toggle
    return window, draw


def reset_all():
    predicting(False)
    cry_toggle()


def continous_detect(window, r):
    predicting(True, True)
    print("stop: ", stop, "; continous_detection: ", continous_detection)
    while stop == False and continous_detection == True:
        print("Continuous Recording iterating")
        r.record(window, lambda: stop)


def single_detect(window, r):
    predicting(True)
    r.record(window, lambda: stop)
    predicting(False)


def main():
    predicting(False)
    window, draw = make_window()

    print("Window Ready!!!")
    r = Record()
    while True:
        print("Ready to read events")
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit', '-ESCAPE-'):
            print('============ Event = ', event, ' ==============')
            print('-------- Values Dictionary (key=value) --------')
            # for key in values:
            #     print(key, ' = ', values[key])
            r.close()
            break

        elif event == "Graph":
            x = values['Graph'][0]
            y = values['Graph'][1]
            print("Graph: ", values["Graph"])
            if 500 < y < 670:
                if 1060 < x < 1215:
                    print("Predicting: Single detection")
                    sd = threading.Thread(
                        target=single_detect, args=(window, r))
                    p = threading.Thread(
                        target=predicting_ring_animation, args=(draw, ))
                    p.start()
                    sd.start()
                elif 1215 < x < 1440:
                    print("Predicting: Continuous detection")
                    cd = threading.Thread(
                        target=continous_detect, args=(window, r,))
                    cd.start()
                    p = threading.Thread(
                        target=predicting_ring_animation, args=(draw, ))
                    p.start()
                elif 1440 < x < 1645:
                    predicting(False)
                    print("Stop recording")
                    print("[LOG] Clicked Stop button!")
                elif 1645 < x < 1797:
                    print("Playback")
                    predicting(False)
                    play_thread = threading.Thread(
                        target=r.play, args=(lambda: stop,))
                    play_thread.start()

            elif 747 < y < 843 and 1311 < x < 1564:
                reset_all()
    window.close()


if __name__ == '__main__':
    main()
    print("\n\nThreads:")
    for thread in threading.enumerate():
        print(thread.name)
