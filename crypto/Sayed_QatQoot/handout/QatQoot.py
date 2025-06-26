from Crypto.Util.number import getPrime, isPrime, bytes_to_long
from secrets import randbelow
import os

class gen:
    def __init__(self, M):
        self.Mod = M
        self.a = randbelow(self.Mod)
        self.x = randbelow(self.Mod)
        self.c = randbelow(self.Mod)
        
    def next(self):
        self.x = (self.a * pow(self.x + self.c, -1, self.Mod)) % self.Mod
        return self.x
    
    
def gen_prime(g, terms):
    while True:
        p = 0
        for _ in range(terms):
            p *= M
            p += g.next()
            
        if isPrime(p):
            return p
        
prime_size = 256
M = getPrime(prime_size)
FLAG = os.getenv("FLAG", "METACTF{A_Hashed_UUID}").encode()

banner = """
 ((      /|_/|
  \\.._.'  , ,\
  /\ | '.__ v /
 (_ .   /   "        
  ) _)._  _ /
 '.\ \|( / ( 
   '' ''\\ \\
       

My cat is sitting on my flag, I can't just force her off though, that's mean!
Can you help me convince her to give it back?
"""

banner2 = """
      _.---.._             _.---...__
   .-'   /\   \          .'  /\     /
   `.   (  )   \        /   (  )   /
     `.  \/   .'\      /`.   \/  .'
       ``---''   )    (   ``---''
               .';.--.;`.
             .' /_...._\ `.
           .'   `.a  a.'   `.
          (        \/        )
           `.___..-'`-..___.'
              \          /
               `-.____.-'
"""
options = """
[1] Give her a Treat
[2] Ask her to give it back
[3] Meow at her
"""


def main():
    print(banner)
    while True:
        print(options)
        choice = input("|> ")
        if choice == "1":
            g = gen(getPrime(prime_size // 2))
            p = gen_prime(g, 2)
            print(f"She chewed it and spat it out :(( but here it is: {p}")
        elif choice == "2":
            g = gen(M)
            p, q = gen_prime(g, 2), gen_prime(g, 2)
            n = p * q
            e = 65537
            m = bytes_to_long(FLAG)
            ct = pow(m, e, n)
            print(f"n: {n}")
            print(f"e: {e}")
            print(f"ct: {ct}")
            print(f"a: {g.a}")
            print(f"c: {g.c}")
        elif choice == "3":
            print(f"Meow! Meow! Meow! Beow! Beow! Beow! \n {banner2}")
            break
        


if __name__ == "__main__":
    main()