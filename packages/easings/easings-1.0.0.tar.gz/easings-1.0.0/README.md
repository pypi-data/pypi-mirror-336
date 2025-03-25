# Easings

## Description

Customizable Optimized Easing Functions for Python.

## Installation

```sh
pip install easings
```

## Usage

Ease values between 0 and 1:

```py
import easings

progress = easings.EaseBack.ease_in_out(
    progress = 0.5,
    bounce_const = easings.EaseBack.in_out_consts[0.1]
)

print(progress)
```

Easing values with a start and end value using an Easer

```py
import easings

easer = easings.Easer(4, 12)

value = easer.value(easings.EasePoly.ease_in_out, 0.5, 2)

print(value)
```

## License

CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.
