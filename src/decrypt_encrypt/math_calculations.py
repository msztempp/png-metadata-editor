import random
import math
from egcd import egcd
import sympy


def is_prime(n):
    return sympy.isprime(n)


def generate_random_prime_number(bit_size):
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
    prime_a = generate_random_prime_number(key_size // 2)
    prime_b = generate_random_prime_number(key_size // 2)
    while prime_a == prime_b:
        prime_b = generate_random_prime_number(key_size // 2)
    return prime_a, prime_b


def miller_rabin_is_prime(number, iterations):
    # Millen-Rabin primality test
    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See https://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    assert type(number) == int, "Number should be int."
    assert number > 2, "Number of iterations should be greater than 2"

    d = number - 1
    s = 0

    while d % 2 == 0:
        s += 1
        d //= 2

    for i in range(iterations):
        a = random.randint(2, number - 2)
        x = pow(a, d, number)
        if x == 1 or x == number - 1:
            continue
        j = 1
        while j < s and x != number - 1:
            x = pow(x, 2, number)
            if x == 1:
                return False
            j += 1
        if x != number - 1:
            return False

    return True


def check_if_prime(number):
    if number > 1:
        for i in range(2, int(number / 2) + 1):
            if (number % i) == 0:
                return False
            break
        else:
            return True
    else:
        return False


def inverse_modulo(a, b):
    x, y, z = extended_euclidean_algorithm(a, b)
    if x != 1:
        raise Exception('modular inverse does not exist')
    else:
        return y % b
