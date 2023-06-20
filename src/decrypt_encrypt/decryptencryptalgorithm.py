import rsa
import math_calculations


class DecryptEncryptAlgorithm:
    def __init__(self, m, key_size=1024):
        self.key_size = key_size
        self.generate_key(m)
        [self.public_key, self.private_key] = rsa.newkeys(key_size)

    # https://www.tutorialspoint.com/cryptography/public_key_encryption.htm#:~:text=Generation%20of%20RSA%20Key%20Pair&text=Calculate%20n%3Dp*q.,a%20minimum%20of%20512%20bits.
    def generate_key(self, m):
        prime_a, prime_b = math_calculations.generate_prime_pair(self.key_size)
        self.public_key = []
        e = None
        n = 0
        while m > n:
            n = prime_a * prime_b
        self.public_key.append(n)
        ed = (prime_a - 1) * (prime_b - 1)
        for e in range(2, ed):
            if math_calculations.greatest_common_divisor(e, ed) == 1:
                self.public_key.append(e)
                break
        print('Public key:', self.public_key)  # [n, e] where n is the modulo and e is the public exponent
        modular_inverse = math_calculations.inverse_modulo(e, ed)
        self.private_key = int(modular_inverse)
        print('Private key:', self.private_key)  # d where d is the private exponent

    def encrypt_from_rsa_module(self, data_to_encrypt, key):
        data_after_encryption = []
        step = self.key_size // 8 - 11  # convert to bytes
        for i in range(0, len(data_to_encrypt), step):


