from numpy import long
from pip._vendor.distlib.compat import raw_input

from helpers import *


def encrypt(sentence, key):   # sentence = string
    encoded = blockConverter(sentence)
    enlength = len(encoded)
    A = long(encoded[0],2)
    B = long(encoded[1],2)
    C = long(encoded[2],2)
    D = long(encoded[3],2)
    orgi = [A,B,C,D]
    r=10
    w=32
    modulo = 2**32
    lgw = 5
    B = (B + key[0]) % modulo
    D = (D + key[1]) % modulo
    for i in range(1,r+1):
        t_temp = (B*(2*B + 1))%modulo 
        t = ROL(t_temp,lgw,32)
        u_temp = (D*(2*D + 1))%modulo
        u = ROL(u_temp,lgw,32)
        tmod=t%32
        umod=u%32
        A = (ROL(A^t,umod,32) + key[2 * i]) % modulo
        C = (ROL(C^u,tmod,32) + key[2 * i + 1]) % modulo
        (A, B, C, D)  =  (B, C, D, A)
    A = (A + key[2 * r + 2]) % modulo
    C = (C + key[2 * r + 3]) % modulo
    cipher = []

    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    return orgi,cipher

