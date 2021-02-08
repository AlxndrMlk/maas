

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