import PySimpleGUI as sg
import numpy as np
import json
import pandas as pd
from data_utils import update_index, get_similarity, compare_authors
from gui_utils import get_label, get_who_codes, get_mark

import time
import os

# Definitions
ID_COL = 'ï»¿IDrec'
FOUND_COLOR = '#243e73'

FEATS = [
    ' ⏪ Prev ',
    ' Next ⏩ ',
    'Go!',
    '-INDEX-',
    '-HUMAN-DECISION-',
    '♻ Google',
    '♻ Scholar',
    '❤ Open PDF',
    '-COMMENT-'
]

# Read in the data
with open(r'./app-data/annotators.dat', 'r') as f:
    ANNOTATORS = f.readlines()

with open(r'./app-data/data.dat', 'r') as f:
    DATA_PATH = f.readline()

data = pd.read_csv(DATA_PATH, sep = ';')
data = data.fillna('')

# Define current index
current_index = 0

# Define theme
sg.theme('DefaultNoMoreNagging')

# Define layout
title_section = [
    [sg.Text('Meta-anaysis assistant', 
        size = (78, 1),
        font = ('Bahnschrift', 16), 
        justification = 'center')],
]


article_section = [
    # Section title
    [sg.Text('\nArticle', font = ('Bahnschrift', 12))],

    # Article ID
    [
        sg.Text('IDrec: ', size = (9, 1)), 
        sg.Input(f'', 
                           size = (8, 1),
                           key = '-INDEX-', 
                           font = 'Halvetica 10',
                           disabled = True),
        sg.Button('Go!', 
            pad = None,
            button_color = 'white on #464b4f', 
            disabled = True,
            use_ttk_buttons = True,
            disabled_button_color = ('white', '#b3b3b3'),
            font = 'Halvetica 8'),

        sg.Text('',
            size = (32, 1),
            text_color = 'red',
            key = '-INDEX-WARNING-')
    ],

    # [sg.Text(font = 'Halvetica 3')],

    # Article titles and authors
    ## Original
    [
        sg.Text('Original', size = (9, 3)),
        sg.Text(f'', 
            size = (48, 3),
            key = '-TITLE-',
            font = 'Halvetica 10 bold')
    ],
    [
        sg.Text('Authors', size = (9, 2)), 
        sg.Text(f'', 
            size = (48, 2),
            key = '-AUTHORS-',
            font = 'Halvetica 10 bold')
    ],

    ## Found
    [
        sg.Text('Found', size = (9, 3)),
        sg.Text(f'⬇⬇⬇ Choose your name and click ▶ Start button ⬇⬇⬇', 
            size = (48, 3),
            key = '-FOUND-TITLE-',
            font = 'Halvetica 10 bold',
            text_color = FOUND_COLOR)
    ],
    [
        sg.Text('Authors', size = (9, 2)), 
        sg.Text(f'', 
            size = (48, 2),
            key = '-FOUND-AUTHORS-',
            font = 'Halvetica 10 bold',
            text_color = FOUND_COLOR)
    ],

    # Articles nav
    ## Search buttons
    [
        sg.Text(size = (16, 1)),

        sg.Button('♻ Google', 
            button_color = 'white on #0096db', 
            use_ttk_buttons = True,
            disabled_button_color = ('white', '#b3b3b3'),
            disabled = True), 

        sg.Button('♻ Scholar', 
            button_color = 'white on #0096db', 
            use_ttk_buttons = True,
            disabled_button_color = ('white', '#b3b3b3'),
            disabled = True), 

        sg.Button('❤ Open PDF', 
            button_color = 'white on #0096db', 
            use_ttk_buttons = True,
            disabled_button_color = ('white', '#b3b3b3'),
            disabled = True),
    ],

    [sg.Text()],
    [
        sg.Text('Titles', size = (12, 1)), 
        sg.Text('',
                size = (3, 1),
                key = '-TITLES-MATCH-',
                font = 'Halvetica 10 bold'), 
        sg.Text(f'', 
                text_color = 'green',
                key = '-TITLES-MATCH-MARK-')
    ],
    [
        sg.Text('Authors', size = (12, 1)), 
        sg.Text('',
                size = (3, 1),
                key = '-AUTHORS-MATCH-',
                font = 'Halvetica 10 bold'),
        sg.Text(f'', 
                text_color = 'green',
                key = '-AUTHORS-MATCH-MARK-')
    ],
    [
        sg.Text('Language', size = (12, 1)), 
        sg.Text(f'0.00',
                size = (3, 1),
                key = '-LANGUAGE-',
                font = 'Halvetica 10 bold',
                text_color = 'gray'),
        sg.Text(f'?', 
                text_color = 'gray',
                key = '-LANGUAGE-MARK-'),
        sg.Text(f'EN', 
                text_color = 'gray',
                key = '-LANGUAGE-NAME-')
    ],
    [
        sg.Text('Article vs book', size = (12, 1)), 
        sg.Text(f'0.00',
                size = (3, 1),
                key = '-IS-A-BOOK-',
                font = 'Halvetica 10 bold',
                text_color = 'gray'),
        sg.Text(f'?', 
                text_color = 'gray',
                key = '-IS-A-BOOK-MARK-'),
        sg.Text(f'NA', 
                text_color = 'gray',
                key = '-IS-A-BOOK-EXPLAIN-')
    ],

    # Nav buttons
    [sg.Text()],
    [
        sg.Combo(ANNOTATORS, background_color = 'green', key = '-ANNOTATORS-', readonly = True), 
        sg.Button('▶ Start', button_color = '#0096db on white', focus = True),
        sg.Text('',
            size = (32, 1),
            text_color = 'red',
            key = '-ANNOTATOR-WARNING-')
    ],

    [
        sg.Text(size = (24, 1)),
        sg.Button(' ⏪ Prev ', disabled = True), 
        sg.Button(' Next ⏩ ', disabled = True), 

    ]
]

decision_section = [

    # MODEL - Section title
    [sg.Text('\nModel', font = ('Bahnschrift', 12))],

    # Model data
    ## Prediction
    [
        sg.Text('Prediction: ', size = (9, 1)),
        sg.Text(f'None', 
                    size = (8, 1),
                    key = '-MODEL-PRED-', 
                    font = 'Halvetica 10 bold')
    ],

    ## Confidence
    [
        sg.Text('Confidence: ', size = (9, 1)),
        sg.Text(f'NA', 
                    size = (8, 1),
                    key = '-MODEL-CONF-', 
                    font = 'Halvetica 10 bold'),
    ],

    # HUMAN - Section title
    [sg.Text('\nHuman', font = ('Bahnschrift', 12))],

    ## Annotator
    [
        sg.Text('Annotator: ', size = (9, 1)),
        sg.Text(f'{get_who_codes(data.at[current_index, "who_codes"])}', 
                    size = (8, 1),
                    key = '-HUMAN-AGENT-', 
                    font = 'Halvetica 10 bold')
    ],

    ## Human decision
    [
        sg.Text('Decision: ', size = (9, 1)),
        sg.Combo([0, 1, 99],
            size = (3, 1),
            background_color = 'green',
            readonly = True,
            default_value = f'{get_label(data.at[current_index, "Final"])}',
            key = '-HUMAN-DECISION-',
            disabled = True)
    ],

    ## Comments
    [sg.Text('\nComments', font = ('Bahnschrift', 12))],
    [
        sg.Multiline(f'{data.at[current_index, "why_not_final"]}',
                     size = (60, 6),
                     key = '-COMMENT-',
                     disabled = True)
    ],

    # Decision buttons
    [sg.Text(size = (1, 1))],
    [
        sg.Text(size = (24, 1)),
        sg.Button('Update ✔', button_color = 'white on green'),
    ],
    [sg.Text(size = (1, 1))],
    [
        sg.Text(size = (25, 1)),
        sg.Button('Quit ❌')
    ]
]



layout = [
    [sg.Column(title_section, size = (900, 50))],
    [sg.Column(article_section),
     sg.VerticalSeparator(),
     sg.Column(decision_section)
    ]
]

# Create the window
window = sg.Window('Meta analysis assistant', layout)

# Define update
def update_screen(window, current_index):
    # Compute vars
    titles_similarity = get_similarity(data.at[current_index, "Title"], data.at[current_index, "web_title"], 2)
    titles_sim_mark = get_mark(titles_similarity, .8)
    authors_match = f'{compare_authors(data.at[current_index, "Authors"], str(data.at[current_index, "web_authors"]).strip().split("-")[0]):.2f}'
    authors_match_mark = get_mark(authors_match, .5)

    # Update data
    window['-INDEX-'].update(f'{data.at[current_index, ID_COL]}')
    window['-TITLE-'].update(f'{data.at[current_index, "Title"].title()}')
    window['-AUTHORS-'].update(f'{data.at[current_index, "Authors"]}')
    window['-FOUND-TITLE-'].update(f'{data.at[current_index, "web_title"]}')
    window['-FOUND-AUTHORS-'].update(f'{str(data.at[current_index, "web_authors"]).strip().split("-")[0].title()}')
    window['-TITLES-MATCH-'].update(f'{titles_similarity:.2f}')
    window['-TITLES-MATCH-MARK-'].update(titles_sim_mark[0], text_color = titles_sim_mark[1])
    window['-AUTHORS-MATCH-'].update(authors_match)
    window['-AUTHORS-MATCH-MARK-'].update(authors_match_mark[0], text_color = authors_match_mark[1])
    #### UPDATE
    # -MODEL-PRED-
    # -MODEL-CONF-
    window['-HUMAN-AGENT-'].update(f'{get_who_codes(data.at[current_index, "who_codes"])}')
    window['-HUMAN-DECISION-'].update(f'{get_label(data.at[current_index, "Final"])}')
    window['-COMMENT-'].update(f'{data.at[current_index, "why_not_final"]}')

    # Update PDF button
    if (data.at[current_index, "pdf_dowloaded"] == 0):
        window['❤ Open PDF'].update(disabled = True)
    else:
        window['❤ Open PDF'].update(disabled = False)


# Loop
while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Quit ❌':
        print('\nThank you for using MAAS!\n')
        break


    if event == '▶ Start':
        
        if len(values['-ANNOTATORS-']) == 0:
            window['-ANNOTATOR-WARNING-'].update('Please choose the annotator!')
        
        else:
            # Warning off
            window['-ANNOTATOR-WARNING-'].update('')

            # Update screen
            update_screen(window, current_index)
            window['▶ Start'].update(disabled = True)
            window['-ANNOTATORS-'].update(disabled = True)

            # Turn on features
            for feat in FEATS:
                window[feat].update(disabled = False)



    if event == 'Go!':
        
        # Get ID values
        new_idx = int(values['-INDEX-'])

        # Check if ID in indices
        if new_idx not in data[ID_COL]:
            # Get nearest valid ID
            argmin = np.argmin(np.abs(data[ID_COL] - new_idx))
            nearest_valid = data.at[argmin, ID_COL]

            # Update warning window
            window['-INDEX-WARNING-'].update(f'No such index! Nearest valid index: {nearest_valid}.')

        else:
            current_index = data[data[ID_COL] == new_idx].index.values[0]
            window['-INDEX-WARNING-'].update('')
            update_screen(window, current_index)


    if event == ' Next ⏩ ':
        
        # Update index
        current_index = update_index(data.index, current_index, 1)

        # Update screen
        update_screen(window, current_index)


    if event == ' ⏪ Prev ':
        
        # Update index
        current_index = update_index(data.index, current_index, -1)

        # Update screen
        update_screen(window, current_index)
        

    if event == '♻ Google':
        search_phrase = f"https://www.google.com/search?q={data.at[current_index, 'web_search_phrase'].replace(' ', '+')}"
        os.system(f"start \"\" {search_phrase}")

    if event == '♻ Scholar':
        search_phrase = f"https://scholar.google.com/scholar?q={data.at[current_index, 'web_search_phrase'].replace(' ', '+')}"
        os.system(f"start \"\" {search_phrase}")

    if event == '❤ Open PDF':
        os.startfile(fr'./pdf-library\\{data.at[current_index, "pdf_dwnld_filename"]}')

    
    if event == 'Update ✔':

        # Store annotator name
        data.at[current_index, 'who_codes'] = values['-ANNOTATORS-']

        # Store decision
        data.at[current_index, 'Final'] = values['-HUMAN-DECISION-']

        # Store comment
        data.at[current_index, 'why_not_final'] = values['-COMMENT-']

        # Store the file
        data.to_csv(DATA_PATH, index = False, sep = ';')

# Finish up by removing from the screen
window.close()