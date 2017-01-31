import random

COLORS = [(253, 185, 19),
          (243, 112, 33),
          (203, 219, 42),
          (250, 157, 0),#voka oranje
          (165, 41, 96),
          (0, 168, 129),
          (0, 154, 218),
          (0, 102, 179)]

def load_background():
    return random.choice(COLORS)
