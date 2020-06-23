class DH_Endpoint(object):
    def __init__(self, generator, prime, private_key):
        self.generator = generator
        self.prime = prime
        self.private_key = private_key
        self.full_key = None

    def generate_partial_key(self):
        partial_key = pow(self.generator, self.private_key, self.prime)  # g**a % p
        return partial_key

    def generate_full_key(self, partial_key_r):
        full_key = pow(partial_key_r, self.private_key, self.prime)  # g**a % p
        self.full_key = full_key
        return full_key

