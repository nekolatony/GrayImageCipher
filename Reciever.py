import pickle
import socket
import threading
import tkinter as tk

import D_H
from CBC_mode import *
from Communication import *
import cv2

HOST, PORT = "localhost", 8000

# a thread class used to update the GUI when the Image is receiver
class App(threading.Thread):

    def __init__(self, tk_root,frame,iframe6,sock,key):
        self.root = tk_root
        self.frame = frame
        self.iframe6 = iframe6
        self.sock = sock
        self.key = key
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        cipherImage = pickle.loads(recv_msg(self.sock))
        cipheredPixels = pickle.loads(recv_msg(self.sock))
        cv2.imwrite("Resources/recivedImagefromServer.png", cipherImage)
        self.iframe6.destroy();
        iframe7 = tk.Frame(self.frame, bd=2, relief=tk.RAISED)
        iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe7, text='Encrypted Image').pack()
        canvas = tk.Canvas(iframe7, width=len(cipherImage[0]) + 20, height=len(cipherImage) + 20)
        B = tk.Button(iframe7, text="Decrypt",
                      command=lambda: startDecrypting(self.root, self.frame, iframe7, cipherImage, cipheredPixels, self.sock,
                                                      self.key)).pack()
        canvas.pack()
        pic1 = tk.PhotoImage(file="Resources/recivedImagefromServer.png")
        canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
        canvas.image = pic1


# callback fuction to decrypt the Image
def startDecrypting(root, frame, iframe6, cipherImage,cipheredPixels, s,key):


    key = key % (2 ** 52)  # gives us key of size 128 bit
    key = str(key)
    RCKey = generateKey(key)

    enc = []
    de = deBlocker(cipheredPixels)
    for i in range(0, len(de), 4):
        enc.append(de[i:i + 4])


    decryptedM = CBC_decrypt(enc, RCKey)

    print('len decrypted ' + str(len(decryptedM)))

    k = 0
    for i in range(len(cipherImage)):
        for j in range(len(cipherImage[0])):
            cipherImage[i][j] = int(decryptedM[k])
            k = k + 1


    cv2.imwrite('Resources/Recieverdecrypted.png', cipherImage)

    iframe6.destroy()
    iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
    iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
    label = tk.Label(iframe7, text='Decrypted Image').pack()
    canvas = tk.Canvas(iframe7, width=len(cipherImage[0]) + 20, height=len(cipherImage) + 20)
    B = tk.Button(iframe7, text="Exit", command=lambda : root.destroy()).pack()
    canvas.pack()
    pic1 = tk.PhotoImage(file="Resources/Recieverdecrypted.png")
    canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
    canvas.image = pic1




def main():
    # Client code:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address = (HOST, PORT)
        s.connect(server_address)

        send_msg(s,pickle.dumps('reciever'))

        DH = D_H.new(14)  # used diffie hellman to get the key used in the encryption
        key = DH.negotiate(s)  # smeding the public key to the reciever and recieving the public key of the reciever

        root = tk.Tk()
        root.title("RECIEVER")
        frame = tk.Frame(root, width=20, height=30, bd=1)
        frame.pack()
        iframe7 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe7.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe7, text='Please wait until the photo is recieved').pack()

        App(root,frame,iframe7,s,key)





        tk.mainloop()

if __name__ == "__main__":
    main()