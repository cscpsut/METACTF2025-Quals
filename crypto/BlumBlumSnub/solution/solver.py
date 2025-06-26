from sage.all import *
from Crypto.Util.number import long_to_bytes, bytes_to_long
from pwn import *
context.log_level = 'DEBUG'


def fermat_factor(n: int, max_steps: int = 1_000_000):
    if n % 2 == 0:
        return (2, n // 2)          


    a = math.isqrt(n)
    if a * a < n:                     
        a += 1

    for _ in range(max_steps):
        b2 = a * a - n                 
        b = math.isqrt(b2)
        if b * b == b2:                
            p = a - b
            q = a + b
            return (min(p, q), max(p, q))
        a += 1                      

    return (1, n)


r = process(["python3", "Meta_testing/blum_blum_shub/chall.py"])

r.recvuntil("n:")
n = int(r.recvline().strip().decode())
r.recvuntil("ct:")
ct = bytes.fromhex(r.recvline().strip().decode())

p, q = fermat_factor(n)


r.recvuntil(": ")
r.sendline("1")
r.recvuntil(": ")
r1 = bytes_to_long(bytes.fromhex(r.recvline().strip().decode()))


r.recvuntil(": ")
r.sendline("1")
r.recvuntil(": ")
r2 = bytes_to_long(bytes.fromhex(r.recvline().strip().decode()))


r.close()

Found = False

def solve(r1, r2, depth = 4):
    global Found
    if Found:
       return
    if depth == 0:
        num = crt([int(r1), int(r2)], [p, q])
        flag = xor(ct, long_to_bytes(num)[:len(ct)])
        print(flag)
        if b"METACTF" in flag:
            print(f"Found flag: {flag.decode()}")
            Found = True
            exit()
        return
    print(f"Solving for r1: {r1}, r2: {r2}, depth: {depth}")
    try:
        roots_p = GF(p)(r1).sqrt(all = True)
        roots_q = GF(q)(r2).sqrt(all = True)
        print(f"Depth: {depth}, Roots p: {roots_p}, Roots q: {roots_q}")
        for rp in roots_p:
            for rq in roots_q:
                solve(int(rp), int(rq), depth - 1)
    except:
        pass


if r1 ** 2 % p == r2:
    print("r1 and r2 are mod p")
elif r1 ** 2 % q == r2:
    print("r1 and r2 are mod q")
else:
    # either r1 is mod p and r2 is mod q, or vice versa
    try:
        rootsq = GF(q)(r2).sqrt(all=True)
        for rq in rootsq:
            solve(r1, int(rq))
    except:
        pass
    try:
        roots_p = GF(p)(r2).sqrt(all=True)
        for rp in roots_p:
            solve(int(rp), r1)
    except:
        pass