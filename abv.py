#!/usr/bin/env python

import argparse
import sys

def validGravity(string) ->float:
    """
    A gravity can be either a four digit number or one digit with three decimals
    The output is the latter
    """
    try:
        fl = float(string)
        pass
    except:
        raise argparse.ArgumentTypeError("Invalid argument " + string + ". Please enter a four digit number or a float with three decimals")
    else:
        if fl >= 1000:
            return fl / 1000
        return fl

def calc(og :float, fg :float) ->float:
    """"
    Calculate final gravity based on SG
    I shamelessly borrowed the alternate formula from this page:
    https://www.brewersfriend.com/2011/06/16/alcohol-by-volume-calculator-updated/
    """
    return (76.08 * ( og - fg )/(1.775 - og)) * (fg / 0.794)

parser = argparse.ArgumentParser(description="Calculate ABV by Gravity")
parser.add_argument("OG", help="The Original Gravity value", type=validGravity)
parser.add_argument("FG", help="The Final Gravity value", type=validGravity)

args = parser.parse_args()
print("Calculated ABV: %2.2f%s" % (calc(args.OG, args.FG), "%"))