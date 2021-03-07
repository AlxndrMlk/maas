import numpy as np
import string
from difflib import SequenceMatcher

def update_index(index_array, current_index, value):
    return np.clip(current_index + value, index_array.min(), index_array.max())


def get_similarity(a, b, round_ = None):

    # To string (if np.nan)
    a = str(a)
    b = str(b)
    
    # Remove punctuation and trans to lowercase
    a = a.translate(str.maketrans('', '', string.punctuation)).lower()
    b = b.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Remove double spaces
    a = ' '.join(a.split())
    b = ' '.join(b.split())
    
    # Cut the longer seq
    len_a = len(a)
    len_b = len(b)
    
    if len_a > len_b:
        a = a[:len_b + 2]
        
    elif len_b > len_a:
        b = b[:len_a + 2]

    ratio = SequenceMatcher(None, a, b).ratio()

    if round_:
        ratio = round(ratio, round_)
    
    return ratio


def compare_authors(original, found):
    original_parsed = []
    found_parsed = []
    
    for oa in str(original.strip()).split(';'):
        
        if len(oa) > 0:
            original_parsed.append(oa.split(',')[0].strip().lower().translate(str.maketrans('', '', string.punctuation)).replace('…', ''))
        
    for fa in str(found.strip()).split(','):
        
        if len(fa) > 0:
            found_parsed.append(fa.split(' ')[-1].strip().lower().translate(str.maketrans('', '', string.punctuation)).replace('…', ''))
        
    diffs = set(original_parsed).difference(set(found_parsed))
        
    return (len(original_parsed) - len(diffs)) / len(original_parsed)


def remove_punctuation(x):
    """
    Takes a string and removes all punctuation.
    """
    return x.translate(str.maketrans('', '', string.punctuation))
