import sys

from numpy import long
from pip._vendor.distlib.compat import raw_input

from helpers import *


def decrypt(encryptedBlock, key):
    encoded = blockConverter(encryptedBlock[0] + encryptedBlock[1] + encryptedBlock[2] + encryptedBlock[3])
    enlength = len(encoded)
    A = long(encoded[0],2)
    B = long(encoded[1],2)
    C = long(encoded[2],2)
    D = long(encoded[3],2)
    cipher = []
    cipher.append(A)
    cipher.append(B)
    cipher.append(C)
    cipher.append(D)
    r=10
    w=32
    modulo = 2**32
    lgw = 5
    C = (C - key[2 * r + 3]) % modulo
    A = (A - key[2 * r + 2]) % modulo
    for j in range(1,r+1):
        i = r+1-j
        (A, B, C, D) = (D, A, B, C)
        u_temp = (D*(2*D + 1))%modulo
        u = ROL(u_temp,lgw,32)
        t_temp = (B*(2*B + 1))%modulo 
        t = ROL(t_temp,lgw,32)
        tmod=t%32
        umod=u%32
        C = (ROR((C - key[2 * i + 1]) % modulo, tmod, 32) ^ u)
        A = (ROR((A - key[2 * i]) % modulo, umod, 32) ^ t)
    D = (D - key[1]) % modulo
    B = (B - key[0]) % modulo
    orgi = []
    orgi.append(A)
    orgi.append(B)
    orgi.append(C)
    orgi.append(D)
    return cipher,orgi


