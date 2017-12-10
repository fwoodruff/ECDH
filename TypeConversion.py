def stringToBigInt(s):
    '''
    maps a string to an integer
    '''
    m=s.encode("hex")
    return int(m, 16)
    
def bigIntToString(i):
    '''
    maps an integer to a string
    '''
    s=hex(i)
    return s[2:-1].decode("hex")

alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'
base_count = len(alphabet)
def intTob58(i):
    '''
    maps an integer to a base-58 string
    '''
    encode = ''  	
    if (i < 0):
        return ''
    while (i >= base_count):	
        mod = i % base_count
        encode = alphabet[mod] + encode
        i = i / base_count
    if (i):
        s58 = alphabet[i] + encode
    return s58
	
def b58toInt(s58):
    '''
    maps a base-58 string to an integer
    '''
    i = 0
    multi = 1
    s58 = s58[::-1]
    for char in s58:
        i += multi * alphabet.index(char)
        multi = multi * base_count	
    return i