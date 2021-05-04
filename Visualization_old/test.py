# import PySimpleGUI as sg
import PySimpleGUIQt as sg

"""
    Demonstration of how to work with multiple colors when outputting text to a multiline element
"""

sg.theme('Dark Blue 3')

def main():

    MLINE_KEY = '-MLINE-'+sg.WRITE_ONLY_KEY

    layout = [  [sg.Text('Demonstration of Multiline Element\'s ability to show multiple colors ')],
                [sg.Multiline(size=(60,20), key=MLINE_KEY)],
                [sg.B('Plain'), sg.Button('Text Blue Line'), sg.Button('Text Green Line')],
                [sg.Button('Background Blue Line'),sg.Button('Background Green Line'), sg.B('White on Green')]  ]

    window = sg.Window('Demonstration of Multicolored Multline Text', layout)

    while True:
        event, values = window.read()       # type: (str, dict)
        print(event, values)
        if event in (None, 'Exit'):
            break
        if 'Text Blue' in event:
            sg.print_to_element(window[MLINE_KEY], 'This is blue text', text_color='blue', end='')
        if 'Text Green' in event:
            sg.print_to_element(window[MLINE_KEY], 'This is green text', text_color='green')
        if 'Background Blue' in event:
            sg.print_to_element(window[MLINE_KEY], 'This is Blue Background', background_color='blue')
        if 'Background Green' in event:
            sg.print_to_element(window[MLINE_KEY], 'This is Green Background', background_color='green')
        if 'White on Green' in event:
            sg.print_to_element(window[MLINE_KEY], 'This is white text on a green background', text_color='white', background_color='green')
        if event == 'Plain':
            sg.print_to_element(window[MLINE_KEY], 'This is plain text with no extra coloring')
    window.close()


if __name__ == '__main__':
    main()
