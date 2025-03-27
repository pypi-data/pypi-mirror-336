import numpy as np


class Catmull():
    def __init__(self, points: np.ndarray, tension = 1.0):
        self.points = points
        self.tension = tension


    def point(self, progress: float):
        i = int(progress)
        local_prog = progress - i
        
        if i < 1:
            i = 1
        elif i > len(self.points) - 3:
            i = len(self.points) - 3
        
        p0, p1, p2, p3 = self.points[i - 1:i + 3]
        
        basis = np.array([1, local_prog, local_prog**2, local_prog**3])
        
        geometry = np.array([
            [0, 1, 0, 0],
            [-self.tension, 0, self.tension, 0],
            [2 * self.tension, self.tension - 3, 3 - 2 * self.tension, -self.tension],
            [-self.tension, 2 - self.tension, self.tension - 2, self.tension]
        ])
        
        return np.dot(basis, np.dot(geometry, np.array([p0, p1, p2, p3])))