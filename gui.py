import PySimpleGUI as sg

# layout = [[sg.Text("Hello from PySimpleGUI")], [sg.Button("OK")]]

# # Create the window
# window = sg.Window("Demo", layout)

# # Create an event loop
# while True:
#     event, values = window.read()
#     # End program if user closes window or
#     # presses the OK button
#     if event == "OK" or event == sg.WIN_CLOSED:
#         break

# window.close()

class GUI:
    def __init__(self) -> None:
        sg.theme("DarkBlue2")

    def welcome_window(self) -> tuple[str, str]:
        """
        Displays a welcome window and requests necessary input

        """
        # Title
        layout = [[sg.Text("Welcome to Othello AI!")]]

        # Choose difficulty
        layout.append([sg.Text("Choose difficulty:")])
        difficulties = ["Novice", "Medium", "Expert"]
        difficulty_row = []
        for difficulty in difficulties:
            difficulty_row.append(sg.Button(difficulty))
        layout.append(difficulty_row)
        diff_input = None

        # Choose color
        layout.append([sg.Text("Choose color! Remember, black goes first...")])
        colors = ["Black", "White"]
        color_row = []
        for color in colors:
            color_row.append(sg.Button(color))
        layout.append(color_row)
        color_input = None

        layout.append([sg.Button("Start", disabled=(diff_input == None) or (color_input == None))])

        # Create window
        window = sg.Window(title="Othello AI", layout=layout)

        # Event loop
        while True:
            event, values = window.read()

            if event == "Start" or event == sg.WIN_CLOSED:
                window.close()
                break

            if event in difficulties:
                diff_input = event
                for diff in difficulties:
                    window[diff].update(disabled=diff != event)
                    window["Start"].update(disabled=(diff_input == None) or (color_input == None))

            if event in colors:
                color_input = event
                for color in colors:
                    window[color].update(disabled=color != event)
                    window["Start"].update(disabled=(diff_input == None) or (color_input == None))

        return (diff_input, color_input)
