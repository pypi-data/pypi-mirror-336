
from pisvp import _core

from pisvp._core import *

import argparse

MODES = (
    'pi64',
    'mc',
    'arctan',
)

def main() -> None:
    parser = argparse.ArgumentParser(
        description='A collection of algorithms for calculating the number π',
        epilog="Keep calm and π on!"
    )
    g1 = parser.add_argument_group('Floating-point computation')
    g1.add_argument("--pi64", action="store_true", default=False, help="builtin f64 value")
    g1.add_argument("--mc", action="store_true", default=False, help="naive Monte Carlo")
    g1.add_argument("--arctan", action="store_true", default=False, help="Taylor series for arctan")

    args = parser.parse_args()

    func = None
    for mode in MODES:
        if getattr(args, mode):
            func = getattr(_core, mode)
            break

    if func is not None:
        print(func())
    else:
        parser.print_help()
