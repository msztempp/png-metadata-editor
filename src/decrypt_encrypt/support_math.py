import random
import math
from egcd import egcd
import sympy


def is_prime(n):
    return sympy.isprime(n)


def generate_random_prime():
    while True:
        num = random.randint(2, 10 ** 6)
        if is_prime(num):
            return num


def greatest_common_divisor(a, b):
    return math.gcd(a, b)


def extended_euclidean_algorithm(a, b):
    return egcd(a, b)


print(is_prime(5))
print(generate_random_prime())
