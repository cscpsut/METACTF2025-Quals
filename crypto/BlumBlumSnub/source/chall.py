from Crypto.Util.number import *
from pwn import xor
import uuid
from hashlib import sha256
import os

print(f'FOR SECURITY REASONS (NOT A HINT I SWEAR) : {sha256(uuid.uuid4().bytes).hexdigest()}')  

FLAG = os.getenv("FLAG", "METACTF{FAKE_FLAG}")

class BlumBlumSnub:
    def __init__(self, p: int, q: int, seed: int = None):
        self.p = p
        self.q = q
        self.m = p * q
        self.state = seed if seed is not None else getRandomInteger(512)

    def next(self) -> int:
        self.state = (self.state * self.state) % self.m
        return self.state 
    
    def get_hint(self) -> bytes:
        x = getRandomInteger(1)
        if x == 0:
            return long_to_bytes(self.next() % self.p)
        else:
            return long_to_bytes(self.next() % self.q)
    
p = getPrime(512)
q = p + 1
while not isPrime(q):
    q += 1

blum_blum_shub = BlumBlumSnub(p, q)

def get_flag():
    return xor(FLAG.encode(), long_to_bytes(blum_blum_shub.next())[:len(FLAG)])

ct = get_flag()

for i in range(3):
    blum_blum_shub.next()

banner = """
      /`·.¸
     /¸...¸`:·
 ¸.·´  ¸   `·.¸.·´)
: © ):´;      ¸  {
 `·.¸ `·  ¸.·´\`·¸)
     `\\´´\¸.·´
     
Welcome to Aqaba!
"""
menu = """
1. Get hint
2. Snub
"""


def main():
    print(banner)
    print(f"n: {blum_blum_shub.m}")
    print(f'ct: {ct.hex()}')
    while True:
        print(menu)
        choice = input("Choose an option: ")
        if choice == '1':
            random_bytes = blum_blum_shub.get_hint()
            print(f"Hint: {random_bytes.hex()}")
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")
            
if __name__ == "__main__":
    main()