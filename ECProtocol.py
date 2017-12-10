''' 
An elliptic curve public key cryptographic protocol for sending messages between two parties.
'''
import TypeConversion as TC
import EllipticCurve as EC
import ECRing
import ECRandom as ECR
import ECbase58 as EC58
import SymmetricCiphers
import KeyGeneration as KG

def encryptSecret(publicKey58,curve):
    '''
    This generates an encrypted random base-58 curve point using the public key.
    '''
    secretPoint = ECR.RandomCurvePoint(curve)
    secret58 = EC58.pointTo58(secretPoint,curve)
    token = ECR.randomNumber()
    publicKeyPoint = EC58.B58toPoint(publicKey58,curve)
    leaderPoint, cipherPoint = curveEncryption(secretPoint,token,publicKeyPoint,curve)
    leader58 = EC58.pointTo58(leaderPoint,curve)
    cipher58 = EC58.pointTo58(cipherPoint,curve)
    return secret58,leader58,cipher58
    
def curveEncryption(P,token,publicKeyPoint,curve):
    '''
    This encrypts a point on the curve using the public key.
    '''
    leaderPoint = ECRing.multiply(token,curve.G,curve)
    pubXtoken = ECRing.multiply(token,publicKeyPoint,curve)
    cipherPoint = ECRing.addPoints(P,pubXtoken,curve)
    return leaderPoint, cipherPoint

def decryptSecret(leader58,cipher58,privateKey58,curve):
    '''
    This recovers the unencrypted point on the curve using the private key.
    '''
    leaderPoint = EC58.B58toPoint(leader58,curve)
    cipherPoint = EC58.B58toPoint(cipher58,curve)
    privateKey = TC.b58toInt(privateKey58[2:])
    decryptedLeaderPoint = ECRing.multiply(-privateKey,leaderPoint,curve)
    secretPoint = ECRing.addPoints(cipherPoint,decryptedLeaderPoint,curve)
    secret58 = EC58.pointTo58(secretPoint,curve)
    return secret58
    
def encryptMessage(message, publicKey58, curve):
    '''
    This encrypts a message.
    '''
    secret58, leader58, cipher58 = encryptSecret(publicKey58, curve)
    SymEncryptedMessage = SymmetricCiphers.XORencrypt(message,secret58[2:])
    return leader58, cipher58, SymEncryptedMessage

def decryptMessage(encryptedMessage58,leader58,cipher58,privateKey,curve):
    '''
    This decrypts a message.
    '''
    secret58 = decryptSecret(leader58,cipher58,privateKey,curve)
    decryptedMessage = SymmetricCiphers.XORdecrypt(encryptedMessage58, secret58[2:])
    return decryptedMessage

if __name__=="__main__":
    # Alice picks an elliptic curve and tells Bob.
    G = ECRing.Point(1,1)
    curve_a = 2
    mercennePower = 521
    curve_p = 2**mercennePower - 1
    curve = EC.EllipticCurve(G,curve_a,curve_p)
    
    # Alice generates a keypair.
    AlicesPrivateKey, AlicesPublicKey = KG.keyPair(curve)
    
    BobsPublicKey = AlicesPublicKey
    print "Alice:\n\'Bob I am using the curve y^2 mod p = x^3 - a x + b mod p for a=%i, b=p-%i, p=2^%i-1, "\
    "(x_0,y_0)=(%i,%i).\nYour public key is %s\'\n"%(curve.a,curve.p-curve.b,mercennePower,curve.G.x,curve.G.y,AlicesPublicKey)

    # Bob encrypts a message with the public key.
    BobsSecretMessage = "Hello Alice."
    BobsLeader,BobsCipher,BobsEncryptedMessage = encryptMessage(BobsSecretMessage,BobsPublicKey, curve)
    
    # Bob sends the secret message to Alice.
    AlicesLeader = BobsLeader
    AlicesCipher = BobsCipher
    AlicesEncryptedMessage = BobsEncryptedMessage
    print 'Bob:\n\'Alice please decrypt this message\nleader:%s\ncipher:%s\nmessage:%s\'\n'%(BobsLeader,BobsCipher,BobsEncryptedMessage)

    # Alice extracts the secret message using her private key.
    AlicesDecryptedMessage = decryptMessage(BobsEncryptedMessage,BobsLeader,BobsCipher,AlicesPrivateKey,curve)
    
    print "__________"
    
    print 'Bob sent \'%s\''% BobsSecretMessage
    print 'Alice received \'%s\''% AlicesDecryptedMessage