import argparse

def ctof(at :float) ->float:
    """ Simple Celsius to Fahrenheit conversion """
    return float(at * (9/5) + 32)


def calc(ar :float, at: float, ct: float) ->float:
    """ Adjust measured SG against the calibration temperature

    param ar float measured gravity
    param at fleat measured temperature
    param ct float calibration temperature
    """
    tf = ctof(at)
    cf = ctof(ct)

    a = 1.00130346
    b = 0.000134722124
    c = 0.00000204052596
    d = 0.00000000232820948

    o = ar * (( a - (b * tf) + (c * pow(tf, 2)) - (d * pow(tf, 3))) / ( a - (b * cf) + (c * pow(cf, 2)) - (d * pow(cf, 3))))
    return round(o * 10000) / 10000

parser = argparse.ArgumentParser(description="Calculate SG correction by temperature")
parser.add_argument('-m', '--measured', help="The measured SG value", type=float, required=True)
parser.add_argument('-t', '--temperature', help="Temperature while measuring", type=float, required=True)
parser.add_argument('-c', '--calibrated-temperature', 
    help="Calculate againt non-default calibrated temperature. The default value is 20 degrees Celsius",
    default=20.0, type=float)

args = parser.parse_args()

print("Adjusted SG: ", calc(args.measured, args.temperature, args.calibrated_temperature))
exit(0)