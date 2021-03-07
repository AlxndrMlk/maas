import numpy as np


def get_label(x):
    try:
        return int(x)
    except ValueError:
        return 'NA'


def get_who_codes(x):
    if len(x.strip()) > 0:
        return x
    else:
        return 'NA'


def get_mark(x, thrshld):
    try:
        if float(x) >= thrshld:
            return '✔', 'green'
        else:
            return '❌', 'red'
    except ValueError:
        return '⚠', 'yellow'


def decode_model_pred(x):
    if x in [0, 1]:
        return str(int(x))
    else: 
        return '--'


def decode_model_error_prob(x, bins, p_error):

    p_error = np.array(p_error)

    try:
        x = float(x)
    except ValueError:
        return 'unknown'

    try:
        proba = p_error[np.digitize(x, bins, right=True) - 1]
        if proba == 0:
            return '< 0.001'
        return f'{proba * 100:.01f}%'
    except IndexError:
        return '--'