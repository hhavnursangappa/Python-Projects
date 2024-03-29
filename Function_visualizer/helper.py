""" Script contains helper functions for the function plotter """
from fractions import Fraction as frac
import numpy as np


def pi_axis_formatter(val, denomlim=10, pi=r'\pi'):
    """
    format label properly
    for example: 0.6666 pi --> 2π/3
               : 0      pi --> 0
               : 0.50   pi --> π/2
    """
    minus = "-" if val < 0 else ""
    val = abs(val)
    ratio = frac(val / np.pi).limit_denominator(denomlim)
    n, d = ratio.numerator, ratio.denominator

    fmt2 = f"{d}"
    if n == 0:
        fmt1 = "0"
    elif n == 1:
        fmt1 = pi
    else:
        fmt1 = f"{n}{pi}"

    fmtstring = "$" + minus + (fmt1 if d == 1 else f"{fmt1}/{fmt2}") + "$"

    return fmtstring
