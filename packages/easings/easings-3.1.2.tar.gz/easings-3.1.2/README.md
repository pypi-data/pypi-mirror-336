# Easings

## Description

Customizable Optimized Library for Easing, Interpolation, Curves and Splines for Python.

## Installation

```sh
pip install easings
```

## Usage

Ease values between 0 and 1:

```py
import easings

progress = easings.back_in_out(
    progress = 0.5,
    bounce_const = easings.both_back_consts[0.1]
)

print(progress)
```

Easing values with a start and end value using an Easer

```py
import easings

easer = easings.Easer(4, 12)

value = easer.value(easings.poly_in_out, 0.5, 2)

print(value)
```

Using a Bezier curve

```py
import numpy as np

import easings

points = np.array([[0, 0], [1, 2], [3, 3], [4, 0]])

curve = easings.curves.Bezier(points)

print(curve.point(0.4))
```

Using a Catmull-Rom spline

```py
import numpy as np

import easings

points = np.array([[0, 0], [1, 2], [2, 4], [3, 3], [4, 1], [5, 2], [6, 0], [7, -1], [8, 1], [9, 3], [10, 2]])

spline = easings.splines.Catmull(points)

print(spline.point(1.2))
```

## License

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.
