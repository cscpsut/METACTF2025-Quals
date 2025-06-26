from Crypto.Util.number import  bytes_to_long as b2l, getPrime
import random
from secret import FLAG

e1 = getPrime(32)
e2 = getPrime(32)

class RSA:
    def __init__(self):        
        self.p = getPrime(2048)
        self.q = getPrime(2048)
        self.N = self.p * self.q
        
    def encrypt(self, m: bytes , e: int) -> list:
        return pow(m, e, self.N)
                        
    def split_blocks(self, m: bytes, Block_Size: int) -> list:
        blocks = []
        for i in range(len(m),-1, -Block_Size):
            if i - Block_Size < 0:
                blocks.append(m[0:i])
            else:
                blocks.append(m[i-Block_Size:i])
        if len(blocks[-1]) == 0:
            blocks.pop()
        return blocks
    
    def pad_block(self, block: bytes) -> list:
        bytelength = int(self.N.bit_length() // 8)
        
        padded = random.randbytes(bytelength - len(block))
        padded += block
        
        return padded


hint = [random.getrandbits(1024) for _ in range(20)]

rsa = RSA()

blocks = rsa.split_blocks(FLAG, 16)
padded_blocks = [b2l(rsa.pad_block(block)) for block in blocks]

cts1 = [rsa.encrypt(pow(block, 120, rsa.N), e1) for block in padded_blocks]
cts2 = [rsa.encrypt(pow(block, 33, rsa.N), e2) for block in padded_blocks]


with open('out.txt', 'w') as f:
    f.write(f'N = {rsa.N}\n')
    f.write(f'c1 = {cts1}\n')
    f.write(f'c2 = {cts2}\n')
    f.write(f'e1 = {e1}\n')
    f.write(f'e2 = {e2}\n')
    f.write(f'hint = {hint}\n')