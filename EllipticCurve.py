class EllipticCurve:
    '''
    y^2 mod p = x^3 + a.x + b mod p
    '''
    def __init__(self, G, a, p):
        self.a = a
        self.p = p
        self.G = G
        self.x0 = G.x
        self.y0 = G.y
        self.b = findCurveB(G,a,p)
        
def findCurveB(G,a,p):
    '''
    y^2 mod p = x^3 + a.x + b mod p
    Finds b given other parameters
    '''
    X = G.x
    Y = G.y
    LHS = (Y*Y) % p
    RHS = (X*X*X + a*X) % p
    b = (LHS - RHS) % p
    return b