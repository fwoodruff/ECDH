import os # for random number generation
import TypeConversion as TC
import ECRing

def randomNumber():
    '''
    Generates a sufficiently large CPRNG
    '''
    a = os.urandom(32)
    rr = TC.stringToBigInt(a)
    return rr

def RandomCurvePoint(curve):
    '''
    This finds a random point on an elliptic curve
    '''
    return ECRing.multiply(randomNumber(),curve.G,curve)