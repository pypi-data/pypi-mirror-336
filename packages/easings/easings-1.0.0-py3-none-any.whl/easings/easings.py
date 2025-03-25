import math

import numba


class EaseSine():
    @numba.njit()
    def ease_in(progress : float):
        return 1 - math.cos((progress * math.pi) / 2)
    

    @numba.njit()
    def ease_out(progress : float):
        return math.sin((progress * math.pi) / 2)
    
    
    @numba.njit()
    def ease_in_out(progress : float):
        return -(math.cos(math.pi * progress) - 1) / 2

    
class EasePoly():
    @numba.njit()
    def ease_in(progress : float, index : float = 2):
        return progress ** index
    
    
    @numba.njit()
    def ease_out(progress : float, index : float = 2):
        return 1 - (1 - progress) ** index
    

    @numba.njit()
    def ease_in_out(progress : float, index : float = 2):
        return 2 ** (index - 1) * progress ** index if progress < 0.5 else 1 - (-2 * progress + 2) ** index / 2
    

class EaseExpo():
    @numba.njit()
    def ease_in(progress : float):
        return 0 if progress == 0 else 2 ** (10 * progress - 10)
    
    
    @numba.njit()
    def ease_out(progress : float):
        return 1 if progress == 1 else 1 - 2 ** (-10 * progress)
    

    @numba.njit()
    def ease_in_out(progress : float):
        return 0 if progress == 0 else 1 if progress == 1 else 2 ** (20 * progress - 10) / 2 if progress < 0.5 else (2 - 2 ** (-20 * progress + 10)) / 2


class EaseCirc():
    @numba.njit()
    def ease_in(progress : float):
        return 1 - (1 - progress * progress) ** 0.5
    

    @numba.njit()
    def ease_out(progress : float):
        return (1 - (progress - 1) * (progress - 1)) ** 0.5
    
    
    @numba.njit()
    def ease_in_out(progress : float):
        return (1 - (1 - (2 * progress) * (2 * progress)) ** 0.5) / 2 if progress < 0.5 else ((1 - (-2 * progress + 2) * (-2 * progress + 2)) ** 0.5 + 1) / 2
    

class EaseBack():
    """
    Constant so the function stretch at max a
    Requires solving this
    3x^2c + 3x^2 - 2cx = 0
    x^3c + x^3 - cx^2 = a
    6(c + 1)x - 2c >= 0
    It's too unclean so I just pre-calculate it instead
    """

    consts = {
        0.1: 1.701540198866823876026881,
        0.2: 2.592388901516299780093093,
        0.3: 3.394051658144560390339483,
        0.4: 4.155744652639193526921365,
        0.5: 4.894859521133737487499187,
        0.6: 5.619622918334312015721260,
        0.7: 6.334566669331999924926985,
        0.8: 7.042439379340939035342756,
        0.9: 7.745023855643342719217190,
        1.0: 8.443535601593252082001106,
    }


    # Double the distance because we normalized
    in_out_consts = {
        0.1: 2.592388901516299780093093,
        0.2: 4.155744652639193526921365,
        0.3: 5.619622918334312015721260,
        0.4: 7.042439379340939035342756,
        0.5: 8.443535601593252082001106,
        0.6: 9.831554964947062296747340,
        0.7: 11.21102691226314259745744,
        0.8: 12.58458023173628922632749,
        0.9: 13.95385474782855076229754,
        1.0: 15.31993028294311226176543
    }


    @numba.njit()
    def ease_in(progress : float, bounce_const : float = 1.701540198866823876026881):
        return (bounce_const + 1) * progress * progress * progress - bounce_const * progress * progress
    

    @numba.njit()
    def ease_out(progress : float, bounce_const : float = 1.701540198866823876026881):
        return (bounce_const + 1) * (progress - 1) ** 3 + bounce_const * (progress - 1) * (progress - 1) + 1


    @numba.njit()
    def ease_in_out(progress : float, bounce_const : float = 2.592388901516299780093093):
        first = ((bounce_const + 1) * (2 * progress) ** 3 - bounce_const * 2 * progress * 2 * progress) / 2
        second = (1 + (bounce_const + 1) * (2 * progress - 2) ** 3 + bounce_const * (2 * progress - 2) ** 2) / 2 + 0.5

        return first if progress < 0.5 else second
    

class EaseElas():
    const_1 = 2 * math.pi / 3
    const_2 = 2 * math.pi / 4.5


    @numba.njit()
    def ease_in(progress : float):
        return 0 if progress == 0 else 1 if progress == 1 else -2 ** (10 * progress - 10) * math.sin((progress * 10 - 10.75) * EaseElas.const_1)
    
    
    @numba.njit()
    def ease_out(progress : float):
        return 0 if progress == 0 else 1 if progress == 1 else 2 ** (-10 * progress) * math.sin((progress * 10 - 0.75) * EaseElas.const_1) + 1
    
    
    @numba.njit()
    def ease_in_out(progress : float):
        first = -(2 ** (20 * progress - 10) * math.sin((20 * progress - 11.125) * EaseElas.const_2)) / 2
        second = (2 ** (-20 * progress + 10) * math.sin((20 * progress - 11.125) * EaseElas.const_2)) / 2 + 1

        return 0 if progress == 0 else 1 if progress == 1 else first if progress < 0.5 else second


class Easer():
    def __init__(self, start_value : float, end_value : float):
        self.start_value = start_value
        self.end_value = end_value


    def value(self, function : callable, progress : float, *args):
        return function(progress, *args) * (self.end_value - self.start_value) + self.start_value
    
    
print(Easer(4, 12).value(EasePoly.ease_in_out, 0.5, 2))