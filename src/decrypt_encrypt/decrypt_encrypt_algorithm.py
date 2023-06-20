import random
from collections import deque

import rsa
import math_calculations


class DecryptEncryptAlgorithm:
    def __init__(self, m, key_size=1024):
        self.key_size = key_size
        self.generate_key(m)
        [self.public_key, self.private_key] = rsa.newkeys(key_size)

        self.encrypted_chunk_size = self.key_size // 8
        self.original_data_length = None
        self.IV=None #initialization vector

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
        block_size_bytes = self.key_size // 8 - 11  # convert to bytes

        for i in range(0, len(data_to_encrypt), block_size_bytes):
            raw_bytes = bytearray(data_to_encrypt[i:i + block_size_bytes])
            input_length = len(raw_bytes)
            bytes_after_encryption = rsa.encrypt(raw_bytes, key)

            for j in range(0, input_length):
                if j < input_length - 1:
                    data_after_encryption.append(bytes_after_encryption[j])
                else:
                    data_after_encryption.append(int.from_bytes(bytes_after_encryption[j:], 'big'))
        return data_after_encryption

    # https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation
    # https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Operation
    # https://www.educative.io/answers/what-is-ecb
    def encrypt_ecb(self, data_to_encrypt):
        cipher_data = []
        after_iend_data = []
        self.original_data_length = len(data_to_encrypt)

        for i in range(0, len(data_to_encrypt), self.encrypted_chunk_size - 1):
            chunk_to_encrypt = bytes(data_to_encrypt[i:i + self.encrypted_chunk_size - 1])

            cipher_int = pow(int.from_bytes(chunk_to_encrypt, 'big'), self.public_key[1], self.public_key[0])
            cipher_bytes = cipher_int.to_bytes(self.encrypted_chunk_size, 'big')

            for j in range(self.encrypted_chunk_size - 1):
                cipher_data.append(cipher_bytes[j])
            after_iend_data.append(cipher_bytes[-1])
        cipher_data.append(after_iend_data.pop())

        return cipher_data, after_iend_data

    def concat_data(self, data, after_iend_data: deque):
        returned_data = []
        for i in range(0, len(data), self.encrypted_chunk_size - 1):
            returned_data.extend(data[i:i + self.encrypted_chunk_size - 1])
            returned_data.append(after_iend_data.popleft())
        returned_data.extend(after_iend_data)
        return returned_data

    def decrypt_ecb(self, data, after_iend_data):
        data_to_decrypt = self.concat_data(data, deque(after_iend_data))
        decrypted_data = []

        for i in range(0, len(data_to_decrypt), self.encrypted_chunk_size):
            chunk_to_decrypt = bytes(data_to_decrypt[i:i + self.encrypted_chunk_size])
            decrypted_int = pow(int.from_bytes(chunk_to_decrypt, 'big'), self.private_key, self.public_key[0])

            # We don't know how long was the last original chunk (no matter what, chunks after encryption have fixed key-length size, so extra bytes could have been added),
            # so below, before creating decrypted_bytes of fixed size we check if adding it to decrypted_data wouldn't exceed the original_data_len
            # If it does, we know that the length of last chunk was smaller and we can retrieve it's length
            if len(decrypted_data) + self.encrypted_chunk_size - 1 > self.original_data_length:
                # last original chunk
                decrypted_length_bytes = self.original_data_length - len(decrypted_data)
            else:
                decrypted_length_bytes = self.encrypted_chunk_size - 1

            decrypted_bytes = decrypted_int.to_bytes(decrypted_length_bytes, 'big')

            for byte in decrypted_bytes:
                decrypted_data.append(byte)

        return decrypted_data

    # https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)
    def encrypt_cbc(self, data_to_encrypt):
        cipher_data=[]
        after_iend_data = []
        self.original_data_length = len(data_to_encrypt)
        self.IV=random.getrandbits(self.key_size)
        prev=self.IV

        for i in range(0, len(data_to_encrypt), self.encrypted_chunk_size - 1):
            chunk_to_encrypt = bytes(data_to_encrypt[i:i + self.encrypted_chunk_size - 1])

            prev=prev.to_bytes(self.encrypted_chunk_size, 'big')
            prev=int.from_bytes(prev[:len(chunk_to_encrypt)],'big')
            xor = int.from_bytes(chunk_to_encrypt, 'big') ^ prev

            cipher_int = pow(xor, self.public_key[1], self.public_key[0])
            prev=cipher_int
            cipher_bytes = cipher_int.to_bytes(self.encrypted_chunk_size, 'big')

            for j in range(self.encrypted_chunk_size - 1):
                cipher_data.append(cipher_bytes[j])
            after_iend_data.append(cipher_bytes[-1])
        cipher_data.append(after_iend_data.pop())

        return cipher_data, after_iend_data
    def decrypt_cbc(self, data, after_iend_data):
        data_to_decrypt = self.concat_data(data, deque(after_iend_data))
        decrypted_data = []
        prev = self.IV

        for i in range(0, len(data_to_decrypt), self.encrypted_chunk_size):
            chunk_to_decrypt = bytes(data_to_decrypt[i:i + self.encrypted_chunk_size])
            decrypted_int = pow(int.from_bytes(chunk_to_decrypt, 'big'), self.private_key, self.public_key[0])

            # We don't know how long was the last original chunk (no matter what, chunks after encryption have fixed key-length size, so extra bytes could have been added),
            # so below, before creating decrypted_bytes of fixed size we check if adding it to decrypted_data wouldn't exceed the original_data_len
            # If it does, we know that the length of last chunk was smaller and we can retrieve it's length
            if len(decrypted_data) + self.encrypted_chunk_size - 1 > self.original_data_length:
                # last original chunk
                decrypted_length_bytes = self.original_data_length - len(decrypted_data)
            else:
                decrypted_length_bytes = self.encrypted_chunk_size - 1

            prev = prev.to_bytes(self.encrypted_chunk_size,'big')
            prev = int.from_bytes(prev[:decrypted_length_bytes],'big')
            xor = prev ^ decrypted_int
            prev=int.from_bytes(chunk_to_decrypt,'big')

            decrypted_bytes = xor.to_bytes(decrypted_length_bytes,'big')

            for byte in decrypted_bytes:
                decrypted_data.append(byte)

        return decrypted_data

    def separate_after_iend(self, cipher_data):
        # ECB with RSA creates slightly bigger IDAT, so we need to put new pixels after IEND
        cipher_data = deque(cipher_data)
        idat_data = []
        after_iend_data = []
        for i in range(self.original_data_length):
            idat_data.append(cipher_data.popleft())
        for i in range(len(cipher_data)):
            after_iend_data.append(cipher_data.popleft())

        return idat_data, after_iend_data

