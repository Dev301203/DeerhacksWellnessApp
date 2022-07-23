import PySimpleGUI as sg

sg.theme('LightBlue3')   # Window Design
# Questions to ask user
layout = [[sg.Text('Wellness Log')],
          [sg.Text("How are you feeling: Enter *good*, *bad*, or *ok*"), sg.InputText()],
          [sg.Text("Have you eaten enough today?"), sg.InputText()], [sg.Text("Have you drunk enough water?"),
          sg.InputText()], [sg.Text("How many times did you press snooze?"), sg.InputText()],
          [sg.Text("Did you leave the house today?"), sg.InputText()],
          [sg.Text("Did you go for walk/spend time outside?"),
          sg.InputText()], [sg.Text("How has your day been from a scale of 1-10?"), sg.InputText()],
          [sg.Text("List 3 things that were good about today:"), sg.InputText()],
          [sg.Text("Note 1 thing you would change:"), sg.InputText()], [sg.Text(size=(40, 1), key='-OUTPUT-')],
          [sg.Button('Ok'), sg.Button('Cancel')]]

# Window Creation
window = sg.Window('Window Title', layout)
# Get all answers from the user
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if window is closed cancelled
        break
    Mood, Eaten, Water, Snooze, House, Walk, = values[0], values[1], values[2], values[3], values[4], values[5]
    Scale, ThreeGood, OneChange = values[6], values[7], values[8]
    window['-OUTPUT-'].update("Daily Log Complete!")
    print(Mood + ', ' + Eaten + ', ' + Water + ', ' + Snooze + ', ' + House + ', ' + Walk + ', ' + Scale +
          ', ' + ThreeGood + ', ' + OneChange)

window.close()


layout = [[sg.Text('Row 1'), sg.Text("What's your name?")],
            [sg.Text('Row 2'), sg.Input()],
            [sg.Text('Row 3'), sg.Button('Ok')]]