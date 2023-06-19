import random
import math
from egcd import egcd
import sympy


def is_prime(n):
    return sympy.isprime(n)


def generate_random_prime(bit_size):
    while True:
        num = random.getrandbits(bit_size)
        if is_prime(num):
            prime_number = num
            return prime_number


def greatest_common_divisor(a, b):
    return math.gcd(a, b)


def extended_euclidean_algorithm(a, b):
    return egcd(a, b)


def generate_prime_pair(key_size):
    prime_a = generate_random_prime(key_size // 2)
    prime_b = generate_random_prime(key_size // 2)
    while prime_a == prime_b:
        prime_b = generate_random_prime(key_size // 2)
    return prime_a, prime_b


def inverse_modulo(a, b):
    x, y, z = extended_euclidean_algorithm(a, b)
    if x != 1:
        raise Exception('modular inverse does not exist')
    else:
        return y % b
