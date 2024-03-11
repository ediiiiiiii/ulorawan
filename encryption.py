import ucryptolib
import ubinascii
import math

def shift_left(data):
    """ Shifts data bytearray left by 1
    """
    for i in range(16):
        if i < 15:
            if (data[i + 1] & 0x80) == 0x80:
                overflow = 1
            else:
                overflow = 0
        else:
            overflow = 0
        # shift 1b left
        data[i] = ((data[i] << 1) + overflow)&0xff

def xor_data(a, b):
    result = bytearray(16)
    for i in range(16):
        result[i] = a[i] ^ b[i]
    return result
            

def generate_subkeys(key):
    """ Generates the k1 and k2 sukeys """
    # K1 generation
    aes = ucryptolib.aes(key, 1)

    k1 = bytearray(16) # 128bit Array
    aes.encrypt(k1, k1)
    flag = k1[0] & 0x80 == 0x80
    shift_left(k1)
    if (flag): k1[15] ^= 0x87
    
    # K2 generation
    k2 = k1[:]
    flag = k2[0] & 0x80 == 0x80
    shift_left(k2)
    if (flag): k2[15] ^= 0x87
    
    return k1, k2

def padding(data):
    """ Adds a padding of a maximum of 16 bytes to a byte array.
    The first padded Bit is a 1."""
    result = bytearray(16)
    result[:len(data)] = data[:]
    padding_start = len(data)
    padding_len = 16 - (padding_start % 16)
    if (padding_len > 0):
        result[padding_start] = 0x80
    for i in range(padding_start+1, 16):
        result[i] = 0x00
    return result

def aes_cmac(key, msg, msg_len):
    """ RFC 4493
        AES 128bit CMAC Algorithm
    """
    k1, k2 = generate_subkeys(key)

    aes = ucryptolib.aes(key, 1) # Mode 1 for ECB 
    n = math.ceil(msg_len / 16.0) # calculate the number of blocks (rounded up)
    
    if n == 0:
        n = 1
        flag = False
    else:
        flag = msg_len % 16 == 0 # flag determines wether the last block is complete
    
    if flag:      
        m_last = xor_data(msg[(n-1)*16:n*16], k1)
        print(ubinascii.hexlify(m_last))
    else:
        m_last = msg[(msg_len//16)*16:msg_len]
        m_last = xor_data(padding(m_last), k2)
           
    result = bytearray(16) # 128-bit array of zeros
    
    for i in range(1, n):
        m_i = msg[(i-1)*16:(i)*16] # get the i-th block
        result = xor_data(result, m_i)
        aes.encrypt(result, result)
        
    aes.encrypt(xor_data(result, m_last), result) # adding the last block
    return result