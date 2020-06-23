import secrets

import cv2 as cv2
import numpy as np
from CBC_mode import *
import tkinter as tk
import venv
import time

def closeWindow(root):
    root.destroy()

def startDecrypting(root, container, innerContainer, cipherImg, cipheredPixels, RCKey, imgMatrix):
     # print("Encrypted pixels (long): " + str(cipheredPixels))

     encryptedWords = []                            # list of string words
     de = deBlocker(cipheredPixels)      # string
     for i in range (0,len(de),4):
         encryptedWords.append(de[i:i+4])

     decryptedImgArray =  CBC_decrypt(encryptedWords,RCKey)
     # print("Decrypted pixels: "+ str(decryptedImgArray))

     decryptedImg = np.empty([len(cipherImg), len(cipherImg[0])], dtype=int)  # long/int

     k = 0
     # print("size of image     = ", str(len(imgMatrix) * len(imgMatrix[0])))
     # print("size of decrepted = ",len(decryptedImgArray))
     for i in range(len(imgMatrix)):
         for j in range(len(imgMatrix[0])):
             decryptedImg[i][j] = int(decryptedImgArray[k])
             k = k + 1
         # print(cipherImage)

     cv2.imwrite('Resources/decrypted.png', decryptedImg)     # saving decrypted image

     innerContainer.destroy()
     newInnerContainer = tk.Frame(container, bd=2, relief=tk.RAISED)
     newInnerContainer.pack(expand=1, fill=tk.X, pady=10, padx=5)
     label = tk.Label(newInnerContainer, text='Decrypted Image').pack()
     canvas = tk.Canvas(newInnerContainer, width=len(imgMatrix[0]) + 20, height=len(imgMatrix) + 20)
     B = tk.Button(newInnerContainer, text="Exit",command = lambda :closeWindow(root)).pack()
     canvas.pack()
     decryptedPic = tk.PhotoImage(file="Resources/decrypted.png")
     canvas.create_image(5, 5, anchor=tk.NW, image=decryptedPic)
     canvas.image = decryptedPic


def startEncrypting(root, container, innerContainer, imageMatrix):   # takes a photo as input and encrypts it with cr6 with CBC mode

    orginalPixels = ConvertImageToStringArray(imageMatrix)    # list of string , each slot is a word of 4 chars ( 4 words = block)
    # print("size of orginalPixels = ", len(orginalPixels))

    a = secrets.randbelow(groups[14][1] - 1)
    b =secrets.randbelow(groups[14][1] - 1)
    print("a = ",a,"\n","b = ",b)
    print("prime = ",groups[14][1])
    user1 = venv.DH_Endpoint(groups[14][0], groups[14][1], a)
    user2 = venv.DH_Endpoint(groups[14][0], groups[14][1],b )
    alicePartialKey = user1.generate_partial_key()
    bobPartialKey = user2.generate_partial_key()
    key = user1.generate_full_key(alicePartialKey)
    key = user2.generate_full_key(bobPartialKey)


    key = key % (2**52)     # gives us key of size 128 bit
    key = str(key)
    print("length of key = ",len(key))
    RCKey = generateKey(key)

    cipheredPixels = CBC_encrypt(orginalPixels, RCKey)   # list of long  //  0.25 the length of the image

    cipherImage = np.empty([len(imageMatrix) , len(imageMatrix[0])], dtype=int)    #long/int

    k = 0
    for i in range(len(cipherImage)):
        for j in range(len(cipherImage[0])):
            cipherImage[i][j] = cipheredPixels[k] % 256
            k = k + 1
    cv2.imwrite('Resources/encrypted.png', cipherImage)


    innerContainer.destroy()
    newInnerContainer = tk.Frame(container, bd=2, relief=tk.RAISED)
    newInnerContainer.pack( expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(newInnerContainer, text='Encrypted Image').pack()
    canvas = tk.Canvas(newInnerContainer, width=len(imageMatrix[0]) + 20, height=len(imageMatrix) + 20)
    B = tk.Button(newInnerContainer, bg = '#85D426', fg = '#e0163b', text="Decrypt", command=lambda: startDecrypting(root, container, newInnerContainer, cipherImage, cipheredPixels, RCKey, imageMatrix)).pack()
    canvas.pack()
    encryptedPic = tk.PhotoImage(file="Resources/encrypted.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=encryptedPic)
    canvas.image = encryptedPic


def main():

    # getting the image,checking its type and saving it in .png format
    url = "Resources/tiger.jpg"
    img = cv2.imread(url,0)
    if img is None:        #Checking if the img is exist
        popupmsg("No photo found!")
        return;
    cv2.imwrite('Resources/activePhoto.png', img)

    root = tk.Tk()                                   # starting gui and opening the image to decrypt
    container = tk.Frame(root, width=len(img[0]) + 20, height=len(img) + 20, bd=1)
    container.pack()

    innerContainer = tk.Frame(container, bd=2, relief=tk.RAISED)
    innerContainer.pack( expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(innerContainer, text='Orginal Image').pack()
    canvas = tk.Canvas(innerContainer, width=len(img[0]) + 20, height=len(img) + 20)
    button = tk.Button(innerContainer,fg = '#85D426',bg = '#e0163b' ,text="Encrypt", command=lambda: startEncrypting(root,container,innerContainer,img)).pack()
    canvas.pack()
    orginalPic = tk.PhotoImage(file="Resources/activePhoto.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=orginalPic)



    tk.mainloop()
if __name__ == "__main__":
    main()