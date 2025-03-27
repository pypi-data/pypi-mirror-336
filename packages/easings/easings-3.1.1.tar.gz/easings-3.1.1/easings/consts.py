import math

import functools


"""
Constant so the function stretch at max a
Requires solving this
3x^2c + 3x^2 - 2cx = 0
x^3c + x^3 - cx^2 = a
6(c + 1)x - 2c >= 0
It's too unclean so 1j just pre-calculate it instead
"""

back_consts = {
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

"""
Credits:
Dinh Tien Hung, classmate, for simplifying the initial equations.
Nguyen Dinh Nguyen, classmate, for simplifying the initial equations.
Of course CGPT for substituting this expression.

Raw expression: c = 9*a/4 - (729*a**2/16 + 81*a/2)/(3*(-1/2 + math.sqrt(3)*1j/2)*(-19683*a**3/64 - 6561*a**2/16 - 729*a/8 + math.sqrt(-4*(729*a**2/16 + 81*a/2)**3 + (-19683*a**3/32 - 6561*a**2/8 - 729*a/4)**2)/2)**(1/3)) - (-1/2 + math.sqrt(3)*1j/2)*(-19683*a**3/64 - 6561*a**2/16 - 729*a/8 + math.sqrt(-4*(729*a**2/16 + 81*a/2)**3 + (-19683*a**3/32 - 6561*a**2/8 - 729*a/4)**2)/2)**(1/3)/3
"""

omega = -1/2 + 3 ** 0.5 / 2 * 1j

@functools.lru_cache(maxsize = 1024)
def calculate_back_const(a : float):
    a_sqr = a * a
    a_cb = a_sqr * a

    s1 = 729/16 * a_sqr + 81/2 * a

    s2 = -19683/32 * a_cb - 6561/8 * a_sqr - 729/4 * a
    s3 = s2 / 2

    delta = (-4 * s1 * s1 * s1 + s2 * s2) ** 0.5

    root = (s3 + delta / 2) ** (1/3)

    omega_root = omega * root

    c = 9/4 * a - s1 / (3 * omega_root) - omega_root / 3

    return c.real

# Double the distance because we normalized
both_back_consts = {
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

elas_const_1 = 2 * math.pi / 3
elas_const_2 = 2 * math.pi / 4.5