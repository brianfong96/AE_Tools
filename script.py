import PySimpleGUI as sg
import calculator

calc = calculator.calculator()

want_column = [
    [
        sg.Text(text="Target Relics")
    ],
    [
        sg.Text(text="Branch"),
        sg.Combo(calc.branches, default_value=calc.branches[0], key='-TARGET-BRANCH-')
    ],
    [
        sg.Text(text="Level"),
        sg.Combo(calc.levels, default_value=calc.levels[0])
    ],    
    [
        sg.Button(button_text="Relic Spot 1", key='-TARGET-RELIC-1-'),
        sg.Button(button_text="Relic Spot 2"),
    ],
    [
        sg.Button(button_text="Relic Spot 3"),
        sg.Button(button_text="Relic Spot 4"),
    ],
    [
        sg.Button(button_text="Relic Spot 5"),
        sg.Button(button_text="Relic Spot 6"),
    ],
    [
        sg.Text(text="Relics", key='-TARGET-RELIC-DISPLAY-')
    ],
]

have_column = [
    [
        sg.Text(text="Current Relics")
    ],
    [
        sg.Text(text="Branch"),
        sg.Combo(calc.branches, default_value=calc.branches[0])
    ],
    [
        sg.Text(text="Level"),
        sg.Combo(calc.levels, default_value=calc.levels[0])
    ],    
    [
        sg.Button(button_text="Relic Spot 1"),
        sg.Button(button_text="Relic Spot 2"),
    ],
    [
        sg.Button(button_text="Relic Spot 3"),
        sg.Button(button_text="Relic Spot 4"),
    ],
    [
        sg.Button(button_text="Relic Spot 5"),
        sg.Button(button_text="Relic Spot 6"),
    ],  
]

essence_column = [
    [
        sg.Text(text="Essence\nHi")
    ],    
]

results_column = [    
    [
        sg.Text(text="Essence Needed =")
    ],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(want_column),
        sg.VSeperator(),
        sg.Column(have_column),
        sg.VSeperator(),
        sg.Column(essence_column),
        sg.VSeperator(),
        sg.Column(results_column)
    ]
]

window = sg.Window("Essence Calculator", layout)

while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    window['-TARGET-RELIC-DISPLAY-'].update(f"{values['-TARGET-BRANCH-']}")
    
    

window.close()