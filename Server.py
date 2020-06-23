import pickle
import socket
import numpy as np
import D_H
from CBC_mode import *
from Communication import *
import cv2
HOST, PORT = "localhost", 8000

# a server class used to connect the sender and the receiver
# it just forwards the reeived messages from each client to the other

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        client1, addr1 = s.accept()
        client2, addr2 = s.accept()
        print(client1)
        print(client2)
        with client1 and client2:
            print('Connected by', addr1)
            print('Connected by', addr2)
            isSender = pickle.loads(recv_msg(client1))
            isReciever =pickle.loads(recv_msg(client2))
            if isSender == 'sender':
                sender = client1
                reciever = client2
            else:
                sender = client2
                reciever = client1
            while True:

                # SenderPublicKey = recv_msg(sender)
                DH = D_H.new(14)  # used diffie hellman to get the key used in the encryption
                # Senderkey= pickle.loads(recv_msg(sender))


                # Senderkey = pickle.loads(recv_msg(sender))
                Senderkey =DH.acceptNegotiation(sender)  # smeding the public key to the reciever and recieving the public key of the reciever
                Senderkey = Senderkey % 2**52
                Senderkey = str(Senderkey)
                RCsenderKey = generateKey(Senderkey)

                print(Senderkey)

                # RecieverPublicKey = recv_msg(reciever)
                DH = D_H.new(14)  # used diffie hellman to get the key used in the encryption
                # Recieverkey = pickle.loads(recv_msg(reciever))

                Recieverkey =DH.acceptNegotiation(reciever)  # smeding the public key to the reciever and recieving the public key of the reciever
                Recieverkey = Recieverkey % 2**52
                Recieverkey = str(Recieverkey)
                RCrecieverKey = generateKey(Recieverkey)

                print(Recieverkey)

                cipherImage = pickle.loads(recv_msg(sender))
                cipherdPixels =pickle.loads(recv_msg(sender))

                #decrypting image

                enc = []
                de = deBlocker(cipherdPixels)
                for i in range(0, len(de), 4):
                    enc.append(de[i:i + 4])
                print(enc)
                decryptedM = CBC_decrypt(enc, RCsenderKey)
                cipherImage1 = np.empty([len(cipherImage), len(cipherImage[0])], dtype=int)
                print(decryptedM)
                k = 0
                for i in range(len(cipherImage1)):
                    for j in range(len(cipherImage1[0])):
                        cipherImage1[i][j] = int(decryptedM[k])
                        k = k + 1

                cv2.imwrite('Resources/Serverdecrypted.png', cipherImage1)


                # encrypting with the reiever key

                orginalPixels = ConvertImageToStringArray(cipherImage1)



                cipheredPixel = CBC_encrypt(orginalPixels, RCrecieverKey)

                img = np.empty([len(cipherImage) , len(cipherImage[0]) ], dtype=int)

                k = 0
                for i in range(len(cipherImage)):
                    for j in range(len(cipherImage[0])):
                        img[i][j] = cipheredPixel[k] % 256
                        k = k + 1

                cv2.imwrite('Resources/Serverencrypted.png', img)

                send_msg(reciever, pickle.dumps(img))
                send_msg(reciever, pickle.dumps(cipheredPixel))
                s.close()

if __name__ == "__main__":
    main()