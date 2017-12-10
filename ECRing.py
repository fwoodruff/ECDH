import ModularOperations as mod

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def addPoints(P,Q,curve):
    '''
    y^2 mod p = x^3 + a.x + b mod p
    Adds points P and Q for a specified elliptic curve
    '''
    p = curve.p
    a = curve.a
    R = Point(p,p) # identity
    if (P.x==p):
        return Q # identity operation
    if (Q.x==p):
        return P
    if (P.x==Q.x and P.y==Q.y):
        modinv2P = mod.modinv((2*P.y)%p,p)
        if modinv2P==p:
            return Point(p,p)
        else:
            s = ((3*(P.x*P.x) + a) * modinv2P) %p
    else:
        modinvPQ = mod.modinv((P.x-Q.x)%p,p)
        if (modinvPQ == p):
            return Point(p,p)
        else:
            s = ((P.y-Q.y) * modinvPQ) %p
        
    R.x = (s*s - P.x - Q.x)%p
    R.y = (-s*s*s + s*(P.x+Q.x) - P.y + s*P.x )%p
    return R
    
def multiply(k,P,curve):
    '''
    y^2 mod p = x^3 + a.x + b mod p
    Multiplies point P by an integer k for a specified elliptic curve
    '''
    p = curve.p
    ls = []
    if (k>=0 or P.x==p):
        Q = P
    else:
        Q = Point(P.x,p-P.y)
        
    kBits = "{0:b}".format(abs(k))
    ls.append(Q)
    for i in range(len(kBits)-1):
        Q=addPoints(Q,Q,curve)
        ls.append(Q)
    R=Point(p,p)
    for i, iK in enumerate(kBits[::-1]):
        if (iK =='1'):
            R=addPoints(R,ls[i],curve)
    return R