import math

from .consts import *


# Sine easing
def sine_in(progress : float):
    return 1 - math.cos((progress * math.pi) / 2)


def sine_out(progress : float):
    return math.sin((progress * math.pi) / 2)


def sine_in_out(progress : float):
    return -(math.cos(math.pi * progress) - 1) / 2

    
# Poly easing
def poly_in(progress : float, index : float = 2):
    return progress ** index


def poly_out(progress : float, index : float = 2):
    return 1 - (1 - progress) ** index


def poly_in_out(progress : float, index : float = 2):
    return 2 ** (index - 1) * progress ** index if progress < 0.5 else 1 - (-2 * progress + 2) ** index / 2
    

# Expo easing
def expo_in(progress : float):
    return 0 if progress == 0 else 2 ** (10 * progress - 10)


def expo_out(progress : float):
    return 1 if progress == 1 else 1 - 2 ** (-10 * progress)


def expo_in_out(progress : float):
    return 0 if progress == 0 else 1 if progress == 1 else 2 ** (20 * progress - 10) / 2 if progress < 0.5 else (2 - 2 ** (-20 * progress + 10)) / 2


# Circ easing
def circ_in(progress : float):
    return 1 - (1 - progress * progress) ** 0.5


def circ_out(progress : float):
    return (1 - (progress - 1) * (progress - 1)) ** 0.5


def circ_in_out(progress : float):
    return (1 - (1 - (2 * progress) * (2 * progress)) ** 0.5) / 2 if progress < 0.5 else ((1 - (-2 * progress + 2) * (-2 * progress + 2)) ** 0.5 + 1) / 2


# Back easing
def back_in(progress : float, bounce_const : float = 1.701540198866823876026881):
    return (bounce_const + 1) * progress * progress * progress - bounce_const * progress * progress


def back_out(progress : float, bounce_const : float = 1.701540198866823876026881):
    return (bounce_const + 1) * (progress - 1) ** 3 + bounce_const * (progress - 1) * (progress - 1) + 1


def back_in_out(progress : float, bounce_const : float = 2.592388901516299780093093):
    first = ((bounce_const + 1) * (2 * progress) ** 3 - bounce_const * 2 * progress * 2 * progress) / 2
    second = (1 + (bounce_const + 1) * (2 * progress - 2) ** 3 + bounce_const * (2 * progress - 2) ** 2) / 2 + 0.5

    return first if progress < 0.5 else second


# Elas easing
def elas_in(progress: float):
    if progress == 0:
        return 0
    if progress == 1:
        return 1
    return -math.exp2(10 * progress - 10) * math.sin((progress * 10 - 10.75) * elas_const_1)


def elas_out(progress: float):
    if progress == 0:
        return 0
    if progress == 1:
        return 1
    return math.exp2(-10 * progress) * math.sin((progress * 10 - 0.75) * elas_const_1) + 1


def elas_in_out(progress: float):
    if progress == 0:
        return 0
    if progress == 1:
        return 1
    if progress < 0.5:
        return -(math.exp2(20 * progress - 10) * math.sin((20 * progress - 11.125) * elas_const_2)) / 2
    return (math.exp2(-20 * progress + 10) * math.sin((20 * progress - 11.125) * elas_const_2)) / 2 + 1


class Easer():
    def __init__(self, start_value : float, end_value : float):
        self.start_value = start_value
        self.end_value = end_value


    def value(self, function : callable, progress : float, *args):
        return function(progress, *args) * (self.end_value - self.start_value) + self.start_value