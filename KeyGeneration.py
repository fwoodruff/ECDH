import TypeConversion as TC
import ECRing
import ECRandom
import ECbase58

def PrivateKey():
    a = ECRandom.randomNumber()
    priv58 = TC.intTob58(a)
    return '01'+priv58
    
def publicKey(privKey58,curve):
    '''
    Computes a public key given a private key and a curve
    '''
    privKey = TC.b58toInt(privKey58[2:])
    pubKeyPoint = ECRing.multiply(privKey,curve.G,curve)
    pubKey58 = ECbase58.pointTo58(pubKeyPoint,curve)
    return pubKey58
    
def keyPair(curve):
    '''
    Produces a private key and a public key for a given curve
    '''
    privKey = PrivateKey()
    pubKey = publicKey(privKey,curve)
    return privKey,pubKey