import random

COLORSGRAY = [(66, 66, 66),
          (33, 33, 2),
          (0, 0, 0)]

COLORSORANGE = [(255, 110, 4),
          (255, 61, 0),
          (255, 87, 34),
          (250, 157, 0)]

IMAGERECHTS = [('R1.jpg'),('R2.jpg'),('R3.jpg')]

def load_GRAY():
    return random.choice(COLORSGRAY)

def load_ORANGE():
    return random.choice(COLORSORANGE)

def load_RECHTS():
    return random.choice(IMAGERECHTS)
