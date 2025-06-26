import string
from Crypto.Util.number import getPrime

chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '{}_!?'
table = {c: i for i, c in enumerate(chars)}


Flag = 'META{TDBtYmFyZGdoaW5pX0d1c3Npbmk}'
def hash(Flag: str) -> str:
    ct = []
    a = getPrime(16)
    b = getPrime(16)

    for i in range(len(Flag)):
        cchar = str((table[Flag[i]])**2 * a + b * a + table[Flag[i]])
        processed = ''
        for j in range(len(cchar)):
            processed += str(chars[int(cchar[j])])
        ct.append(processed)
        if i % 2 == 1 :
            a = getPrime(16)
            b = getPrime(16)
    return "-".join(ct)
    
with open('out.txt', 'w') as f:
    f.write(f'MySuperSecretHash = {hash(Flag)}')

