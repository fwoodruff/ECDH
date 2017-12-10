import TypeConversion as TC
import ModularOperations as mod
import ECRing

def pointTo58(P,curve):
    '''
    maps a point to a base-58 string
    '''
    key58 = TC.intTob58(P.x)
    if (P.y>(curve.p/2)):
        return '03'+key58
    else:
        return '02'+key58
    
def B58toPoint(P58,curve):
    '''
    maps a base-58 string to a point
    '''
    a = curve.a
    p = curve.p
    b = curve.b

    keyX = TC.b58toInt(P58[2:])
    keyYsq = (keyX*keyX*keyX + a*keyX + b)%p
    keyY = mod.modular_sqrt(keyYsq,p)
    
    if (P58[0]=='0' and P58[1]=='3'):
        if (keyY>curve.p/2): 
            return ECRing.Point(keyX,keyY)
        else:
            return ECRing.Point(keyX,p-keyY)
    else:
        if (keyY>curve.p/2): 
            return ECRing.Point(keyX,p-keyY)
        else:
            return ECRing.Point(keyX,keyY)