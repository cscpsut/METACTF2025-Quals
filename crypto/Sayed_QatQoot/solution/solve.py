from Crypto.Util.number import isPrime, long_to_bytes
from sage.all import *
from secrets import randbelow
from Crypto.Util.number import getPrime
from tqdm import tqdm
from pwn import *
context.log_level = 'DEBUG'

def get_prime():
    r.recvuntil("|> ")
    r.sendline("1")
    r.recvuntil("but here it is: ")
    return int(r.recvline().strip().decode())


r = process(["python3", "Meta_testing/QCG/chall_final.py"])
primes = [get_prime() for _ in range(5)]

from ACD import ACD
m = int(ACD(primes, 256))
print(f"m: {m}")
assert isPrime(m)

# LCG parameters
r.recvuntil("|> ")
r.sendline("2")
r.recvuntil("n: ")
n = int(r.recvline().strip().decode())

r.recvuntil("e: ")
e = int(r.recvline().strip().decode())

r.recvuntil("ct: ")
ct = int(r.recvline().strip().decode())

r.recvuntil("a: ")
a = int(r.recvline().strip().decode())
r.recvuntil("c: ")
c = int(r.recvline().strip().decode())

def prev(x_next, a, c, M):
    return (a * pow(x_next, -1, M) - c) % M

def get_xk(x0_val, k, a, c, M):
    R = Zmod(M)
    A = Matrix(R, [[0, a], [1, c]])
    Ak = A**k
    num = (Ak[0, 0] * x0_val + Ak[0, 1])
    den = (Ak[1, 0] * x0_val + Ak[1, 1])
    if den == 0:
        raise ZeroDivisionError("Denominator in Möbius transformation is zero.")
    return (num / den)

x0x1 = n % m

for k in tqdm(range(4000)):
    try:
        R = Zmod(m)
        PR = PolynomialRing(R, 'x0')
        x0 = PR.gen()
        num = get_xk(x0, k, a, c, m).numerator()
        den = get_xk(x0, k, a, c, m).denominator()
        f = x0 * num  - x0x1 * den
        
        if f.is_zero():
            continue
        roots = f.roots()
        
        print(f"Roots found: {roots}")
        
        for root, mult in roots:
            x0_val = int(root)
            p = prev(x0_val, a, c, m) * m + x0_val
            if gcd(p, n) == p:
                print(f"Found prime p: {p}")
                q = n // p
                print(f"Found prime q: {q}")
                phi = (p - 1) * (q - 1)
                d = pow(e, -1, phi)
                msg = pow(ct, d, n)
                flag = long_to_bytes(msg)
                print(flag)
                exit(0)
        print(f"No valid roots found for k={k}")
    except Exception as e:
        print(f"Unexpected error at k={k}: {e}")
        continue