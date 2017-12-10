import TypeConversion as TC

def XORencrypt(message, symmetricKey58):
    '''
    XOR encrypts a message using a symmetric key
    '''
    messageID = TC.stringToBigInt(message)
    symmetricKeyID = TC.b58toInt(symmetricKey58)
    encryptedMessageID = messageID ^ symmetricKeyID
    encryptedMessage58 = TC.intTob58(encryptedMessageID)
    return encryptedMessage58
    
def XORdecrypt(encryptedMessage58, symmetricKey58):
    '''
    XOR decrypts a message using a symmetric key
    '''
    messageInt = TC.b58toInt(encryptedMessage58)
    symmetricKeyInt = TC.b58toInt(symmetricKey58)
    decryptedMessageInt = messageInt ^ symmetricKeyInt
    decryptedMessage = TC.bigIntToString(decryptedMessageInt)
    return decryptedMessage