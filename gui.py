from datetime import datetime

import PySimpleGUI as sg

import quickstart


def get_data():
    sg.theme('LightBlue3')  # Window Design
    # Questions to ask user
    layout = [[sg.Text('Wellness Log', font="bold")],
              [sg.Text("1. How are you feeling?"), sg.Combo(values=[
                  "Bad : (",
                  "Okay : |",
                  "Good : )"
              ], size=50)],
              [sg.Text("2. Have you eaten enough today?"), sg.Checkbox("")],
              [sg.Text("3. Have you drank enough water?"), sg.Checkbox("")],
              [sg.Text("4. Did you get enough sleep?"), sg.Checkbox("")],
              [sg.Text("5. Did you leave the house today?"), sg.Checkbox("")],
              [sg.Text("6. How has your day been from a scale of 1-10?"),
               sg.InputText()],
              [sg.Text("7. Note thing that was good about today:"),
               sg.InputText()],
              [sg.Text("8. Note 1 thing you would change:"), sg.InputText()],
              [sg.Text(size=(40, 1), key='-OUTPUT-')],
              [sg.Button('Ok'), sg.Button('Cancel'), sg.Button("History")]]

    history_layout = []

    service = quickstart.start_authentication()
    wellness_history = quickstart.get_document_data()
    # Window Creation
    window = sg.Window('Wellness Log', layout)
    # Get all answers from the user
    while True:
        valid = True
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if window is closed
            # cancelled
            break
        if event == "Ok":
            Mood, Eaten, Water, Snooze, House, = values[0], values[1], values[
                2], values[3], values[4]
            Scale, ThreeGood, OneChange = values[5], values[6], values[7]

            try:
                scaledummy = int(Scale)
                if not 10 >= scaledummy >= 1:
                    valid = False
                    print(
                        "Question 7 inputted incorrectly, make sure it's a "
                        "number "
                        "between 1-10!")
            except ValueError:
                valid = False
                print(
                    "Question 7 inputted incorrectly, make sure it's a number!")

            if valid:
                window['-OUTPUT-'].update("Daily Log Complete!")
                todays_info = {
                    "date": datetime.today().strftime('%Y-%m-%d'),
                    "mood": Mood,
                    "eaten": "Yes" if Eaten else "No",
                    "water": "Yes" if Water else "No",
                    "snooze": "Yes" if Snooze else "No",
                    "house": "Yes" if House else "No",
                    "scale": Scale,
                    "threeGood": ThreeGood,
                    "oneChange": OneChange
                }
                print(todays_info)
                wellness_history.insert(0, todays_info)
                quickstart.update_cloud_document(service, str(wellness_history))
            if not valid:
                continue
        elif event == "History":
            open_history_window(wellness_history)


def open_history_window(wellness_history):
    table_headings = [
        "Date",
        "Mood",
        "Did you eat?",
        "Did you drink water?",
        "Sleep well",
        "Left house",
        "Rating",
        "3 good things",
        "What would you change"
    ]
    table_values = []
    for point in wellness_history:
        row = []
        row.append(point["date"])
        row.append(point["mood"])
        row.append(point["eaten"])
        row.append(point["water"])
        row.append(point["snooze"])
        row.append(point["house"])
        row.append(point["scale"])
        row.append(point["threeGood"])
        row.append(point["oneChange"])
        table_values.append(row)
    layout = [[sg.Table(values=table_values, headings=table_headings)]]

    window = sg.Window("History", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()
