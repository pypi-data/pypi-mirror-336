import numpy as np

# Globals
CHARGE_DICT = {
  "A": 0,
  "C": 0,
  "D": -1,
  "E": -1,
  "F": 0,
  "G": 0,
  "H": 0,
  "I": 0,
  "K": .2, 
  "L": 0,
  "M": 0,
  "N": 0,
  "P": 0,
  "Q": 0,
  "R": .2,
  "S": 0,
  "T": 0,
  "V": 0,
  "W": 0,
  "Y": 0,
  "$": -2, # phosphoserine
}

VOLUME_DICT = {
  "A": 60.4,
  "C": 73.4,
  "D": 73.8,
  "E": 85.9,
  "F": 121.2,
  "G": 43.2,
  "H": 98.8,
  "I": 107.5,
  "K": 108.5,
  "L": 107.5,
  "M": 105.3,
  "N": 78,
  "P": 81,
  "Q": 93.9,
  "R": 127.3,
  "S": 60.3,
  "T": 76.8,
  "V": 90.8,
  "W": 143.9,
  "Y": 123.1,
  "$": 126.5761595169 # phosphoserine
}

# WINDOW_SIZE = 20 # don't adjust without also fixing the parabola in predict_current
# def predict_current(window):
#     # Window function is a parabola with width 20 and height 1
#     window_indices = np.arange(WINDOW_SIZE)
#     window_function = -0.00944976*window_indices**2 + 0.179545*window_indices + 0.148364
#     volume_score = sum([VOLUME_DICT[x] for x in window]*window_function)
#     charge_score = sum([CHARGE_DICT[x] for x in window]*window_function)
#     volume_coeff = 0.00390066
#     charge_coeff = 0.40828262
#     return 1-(volume_coeff*volume_score+charge_coeff*charge_score)

# def template_from_sequence(seq):
#     reversed_seq = seq[::-1]
#     squiggle = [predict_current(reversed_seq[i:i+WINDOW_SIZE]) for i in range(0, len(reversed_seq)-WINDOW_SIZE+1)]
#     return np.array(squiggle)

window_size = 20
window_indices = np.arange(window_size)
window_function = np.array(-0.00944976 * window_indices**2 + 0.179545 * window_indices + 0.148364, dtype=np.float64)
volume_coeff = 0.00390066
charge_coeff = 0.40828262

def get_score(amino_acid):
  return volume_coeff*VOLUME_DICT[amino_acid] + charge_coeff*CHARGE_DICT[amino_acid]

def predict_current(window):
    scores = [get_score(x) for x in window]
    # Compute volume_score and charge_score using numpy dot product
    window_score = np.dot(scores, window_function)
    return 1 - window_score

def template_from_sequence(seq):
    backwards_sliding_indices = range(len(seq) - window_size, -1, -1)
    squiggle = np.array([predict_current(seq[i:i+window_size]) for i in backwards_sliding_indices], dtype=np.float64)
    return squiggle