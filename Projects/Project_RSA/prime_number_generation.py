import random
import sys
from time import time


# You will need to implement this function and change the return value.
def mod_exp(x: int, y: int, N: int) -> int:
    if (y == 0):
        return 1
    z = mod_exp(x,y//2,N)
    if (y % 2 == 0):
        return (z * z) % N
    else:
        return (x * (z * z) % N)


def fermat(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    for i in range(k):
        pos_prime = random.randint(2, N - 2)
        if mod_exp(pos_prime, N - 1, N) != 1:
            return False
    return True



def miller_rabin(N: int, k: int) -> bool:
    """
    Returns True if N is prime
    """
    if N < 2 or N % 2 == 0:
        return False
    if N in (2, 3):
        return True
    d = N - 1
    s = 0
    while d % 2 == 0:
        d = d//2
        s += 1
    for i in range(k):
        a = random.randrange(2, N - 1)
        x = mod_exp(a, d, N)
        if x == 1 or x == N - 1:
            continue
        for j in range(s - 1):
            x = (x * x) % N
            if x == N - 1:
                break
            else:
                return False
    return True


def generate_large_prime(n_bits: int) -> int:
    """Generate a random prime number with the specified bit length"""
    while True:
        candidate = random.getrandbits(n_bits)
        candidate |= (1 << (n_bits - 1))
        candidate |= 1
        if fermat(candidate, 20):
            if miller_rabin(candidate, 20):
                return candidate


def main(n_bits: int):
    start = time()
    large_prime = generate_large_prime(n_bits)
    print(large_prime)
    print(f'Generation took {time() - start} seconds')


if __name__ == '__main__':
    main(int(sys.argv[1]))
