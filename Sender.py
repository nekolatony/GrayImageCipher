import pickle
import queue as Queue
import socket
import threading
import time
from tkinter.filedialog import askopenfilename
from tkinter.ttk import *
import numpy as np
import cv2

import D_H
from CBC_mode import *
from Communication import *

HOST, PORT = "localhost", 8000



# the GUI and encrypting thread communcate throug a queue
# the GUI calls this function once every 100 millisecond to check if the
#encryption has finished so that it can update the GUI accordingly
def process_queue(root,frame,img,q):
    try:
        msg = q.get(0)
        frame = tk.Frame(root, width=20, height=20, bd=1)
        frame.place(x= 0,y = 0)
        iframe6 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe6.pack(expand=1, fill=tk.X, pady=10, padx=5)
        B = tk.Button(iframe6, text="Exit", command=lambda: root.destroy()).pack()
        label = tk.Label(iframe6, text='Original Image').pack()
        canvas = tk.Canvas(iframe6, width=len(img[0]) + 20, height=len(img) + 20)
        canvas.pack()
        pic1 = tk.PhotoImage(file="Resources/original.png")
        canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
        canvas.image = pic1
        root.update_idletasks()


    except Queue.Empty:
        root.after(100, lambda:process_queue(root,frame,img,q))

# thread class used to encypt the Image so that the GUI does'nt freeze while encrypting
class App(threading.Thread):

    def __init__(self,root,q,prgress,sock,frame,iframe5,img,key):
        self.root = root
        self.frame = frame
        self.iframe5 = iframe5
        self.sock = sock
        self.img = img
        self.progress = prgress
        self.q = q
        self.key = key
        threading.Thread.__init__(self)
        self.start()

    # encrypts the Image in a thread
    def run(self):
        orginalPixels = ConvertImageToStringArray(self.img)
        print(len(orginalPixels))


        self.key = str(self.key)

        if len(self.key) < 16:
            self.key = self.key + " " * (16 - len(self.key))
        self.key = self.key[:16]
        self.progress['value'] = 10
        self.root.update_idletasks()

        RCKey = generateKey(self.key)
        print(orginalPixels)

        encrypted = []
        cipheredPixels = CBC_encrypt(orginalPixels, RCKey)

        self.progress['value'] = 20
        self.root.update_idletasks()
        time.sleep(0.1)
        self.progress['value'] = 30
        self.root.update_idletasks()
        time.sleep(0.1)

        cipherImage = np.empty([len(self.img), len(self.img[0])], dtype=int)

        self.progress['value'] = 40
        self.root.update_idletasks()
        time.sleep(0.1)
        self.progress['value'] = 60
        self.root.update_idletasks()
        time.sleep(0.1)

        k = 0
        flag = 0
        for i in range(len(self.img)):
            for j in range(len(self.img[0])):
                cipherImage[i][j] = cipheredPixels[k] % 256
                flag = flag + 1
                if flag == 4 :
                    k = k + 1
                    flag = 0

        self.progress['value'] = 80
        self.root.update_idletasks()
        time.sleep(0.1)

        self.progress['value'] = 100
        self.root.update_idletasks()
        time.sleep(0.1)

        cv2.imwrite('Resources/encrypted.png', cipherImage)
        print('len original' + str(len(orginalPixels)))

        BcipherImage = pickle.dumps(cipherImage)
        BcipheredPixel = pickle.dumps(cipheredPixels)
        send_msg(self.sock, BcipherImage)
        send_msg(self.sock, BcipheredPixel)

        self.q.put("Task finished")


#callback funtion to start encrypting
# uses threading so that the GUI doesn't freeze during encryption
def startEncrypting(root, frame, iframe5, img, sock, progress,key):
    q = Queue.Queue()

    App(root,q,progress,sock,frame,iframe5,img,key)
    root.after(50,lambda :process_queue(root,frame,img,q))


#callback funtion for opining the file chooser
def OpenPicture(root, frame, iframe5, s,key):
    url = askopenfilename()
    print(url)
    if url.endswith(".png") or url.endswith(".jpg"):
        img = cv2.imread(url, 0)
        cv2.imwrite("Resources/original.png", img)
        img = cv2.imread('Resources/original.png', 0)
        url = 'Resources/original.png'
        iframe5.destroy()

        iframe6 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe6.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe6, text='Orginal Image').pack()
        canvas = tk.Canvas(iframe6, width=len(img[0]) + 20, height=len(img) + 30)
        B = tk.Button(iframe6, fg='#85D426', bg='#e0163b', text="Encrypt and SEND",
                      command=lambda: startEncrypting(root, frame, iframe6, img, s,
                                                      progress,key)).pack()
        global pic1
        pic1 = tk.PhotoImage(file=url)
        canvas.create_image(5, 5, anchor=tk.NW, image=pic1)
        progress = Progressbar(iframe6, orient=tk.HORIZONTAL,
                               length=100, mode='determinate')
        canvas.pack()

        progress.pack(pady=10)





def main():
    # Client code:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        server_address = (HOST, PORT)
        s.connect(server_address)


        send_msg(s,pickle.dumps('sender'))   # the sender announces himself to the server

        DH = D_H.new(14)       # used diffie hellman to get the key used in the encryption
        key = DH.negotiate(s)   # sending the public key to the reciever and recieving the public key of the reciever
        key = key % (2 ** 52)  # gives us key of size 128 bit
        key = str(key)

        root = tk.Tk()
        root.title("SENDER")
        frame = tk.Frame(root, width=20, height=20, bd=1)
        frame.pack()
        iframe5 = tk.Frame(frame, bd=2, relief=tk.RAISED)
        iframe5.pack(expand=1, fill=tk.X, pady=10, padx=5)
        label = tk.Label(iframe5, text='Please choose picture to encrypt and send').pack()
        B = tk.Button(iframe5, fg='#85D426', bg='#e0163b', text="Open File",
                      command=lambda: OpenPicture(root, frame, iframe5, s,key)).pack()

        tk.mainloop()


if __name__ == "__main__":
    main()
