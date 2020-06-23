from encrypt import *
from decrypt import *
from helpers import *


IV = "123456789abcdefg"


#Key add (CBC takes a key to perform encryption)
def CBC_encrypt(message,key):
    words = message
    xoredBlock = xor_two_str(words[0]+words[1]+words[2]+words[3] , IV)

    orgin,encrypted_block = encrypt(xoredBlock, key)    # cr6
    cipherMessage = list(encrypted_block[0:])

    for k in range(4, len(words) , 4):   # xor each block with the prev encrypted block and ecrypt it and save it to cipherMessage
        xoredBlock = xor_two_str(words[k] + words[k+1] + words[k+2] + words[k+3], deBlocker(encrypted_block))


        orgi,encrypted_block = encrypt(xoredBlock, key)
        cipherMessage.append(encrypted_block[0])
        cipherMessage.append(encrypted_block[1])
        cipherMessage.append(encrypted_block[2])
        cipherMessage.append(encrypted_block[3])
        # print("encryption number " + str(k))
    print("size of cipherMessage = ", len(cipherMessage))

    return cipherMessage    # list of long



#Key add (CBC takes a key to perform decryption)
def CBC_decrypt(cipher, key):
    words = cipher
    print("********************************DECRYPTING*********************************")
    orgi,decrypted_block = decrypt((words[0:4]), key)

    unXoredBlock = xor_two_str(deBlocker(decrypted_block), IV)
    orginal = [unXoredBlock[:4],unXoredBlock[4:8],unXoredBlock[8:12],unXoredBlock[12:16]]

    for k in range(4, len(words) , 4):
        orgi,decrypted_block = decrypt((words[k:k + 4]), key)
        unXoredBlock = xor_two_str(words[k-4]+ words[k-3] + words[k-2] + words[k-1], deBlocker(decrypted_block))

        orginal.append(unXoredBlock[:4])
        orginal.append(unXoredBlock[4:8])
        orginal.append(unXoredBlock[8:12])
        orginal.append(unXoredBlock[12:16])
        # print("decryption number " + str(k))
    print("size of orginal = ", len(orginal))

    return  orginal
