import pickle
import secrets

from Communication import *

from helpers import groups

class DHE(object):
    """ DHE object
    __init__(group=14, randInt=randint):
        - initializes the object and generates the local secret (a)
        group: a group number as per RFC 3526 (default: 14 - 2048 bits)
        randInt: a callable that returns random numbers.
    getPublicKey():
        - returns your public key (i.e. g**a % p)
    update(B):
        - accepts the public key (B) from remote party,
        generates, and returns final shared key ( i.e. B**a % p)
    getFinalKey():
        - returns final shared key
        REQUIRES update() to be called prior.
        otherwise, throws ValueError
    negotiate(sock):
        - sends Public key via sock.send()
        receives other party's Public key via sock.recv(1024)
        calls update() and returns value
    """

    def __init__(self, group=14):
        self.group = group

        # I could use nested try statements
        # or I could use isinstance with if-elif-else
        # I chose the latter, if you disagree, submit an issue
        if isinstance(group, int):
            self.g = groups[group][0]
            self.p = groups[group][1]

        else:
            raise TypeError("{} is not an int"
            .format(group))

        self.a = secrets.randbelow(self.p - 1)
        self.public = pow(self.g, self.a, self.p)  # g**a % p
        self.key = 0


    def getPublicKey(self):
        return self.public

    def update(self, B):
        self.key = pow(B, self.a, self.p)  # B**a % p == g**ba % p
        return self.key

    def getFinalKey(self):
        if self.key:
            return self.key

        raise ValueError(
            "Incomplete Key: please call update() with public key")

    def negotiate(self, sock):
        send_msg(sock,pickle.dumps(self.getPublicKey()))
        B = pickle.loads(recv_msg(sock))
        return self.update(B)

    def acceptNegotiation(self, sock):
        B = pickle.loads(recv_msg(sock))
        send_msg(sock,pickle.dumps(self.getPublicKey()))
        return self.update(B)


def new(*args, **kwargs):
    return DHE(14)
