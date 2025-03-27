import math
import numpy as np


class CubicBezier():
    def __init__(self, points : np.ndarray):
        self.points = points

    
    def point(self, prog : float):
        prog_cp = 1 - prog

        basis = np.empty(self.points.shape[0])

        for i in range(self.points.shape[0]):
            basis[i] = math.comb(self.points.shape[0] - 1, i) * prog_cp ** (self.points.shape[0] - 1 - i) * prog ** i
        
        return basis @ self.points