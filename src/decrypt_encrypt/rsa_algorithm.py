import rsa
import support_math


class RSAAlgorithm:

    def __init__(self, tmp, key_size=1024):
        self.key_size = key_size
        self.generate_key(tmp)
        [self.public_key, self.private_key] = rsa.newkeys(key_size)

    def generate_key(self, tmp):
        pass
