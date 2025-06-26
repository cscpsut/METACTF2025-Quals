from sage.all import *


def ACD(choice, prime_size):
    X = 2 ** (prime_size >> 1)
    samples = len(choice)
    m = Matrix(ZZ, samples + 1, samples + 1)

    m[0, 0] = X
    for i in range(1, samples + 1):
        m[0, i] = choice[i - 1]
        m[i, i] = choice[0]

    reduced = m.LLL()
    q0 = abs(reduced[0, 0] // X)
    r0 = choice[0] % q0
    return round((choice[0] - r0) / q0)
