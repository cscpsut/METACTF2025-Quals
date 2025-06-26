
dword_620 = [
    0x8fb09b5d,0x47691155,0x14b03245,0x2305d451, 0x1133B6D3,
    0x14B03245, 0x6C444296, 0x06AC0A28, 0x0C3AADA7, 0x15219CE6,
    0x0F744EB8E, 0x0CE758020, 0x3E0CCF25, 0x84B79271, 0x2802DD7D,
    0x3119EC3C, 0x0CBF604B6, 0x0CE758020, 0x0F744EB8E, 0x7E587AFB,
    0x813416E7, 0x0F744EB8E, 0x813416E7, 0x2802DD7D, 0x32F8EBE,
    0x0CBF604B6, 0x0F744EB8E, 0x1A34BFFF, 0x0D2ED35F7, 0x0F744EB8E,
    0x0C3AADA7, 0x15219CE6, 0x0F744EB8E, 0x0CE758020, 0x3E0CCF25,
    0x84B79271, 0x15219CE6, 0x3119EC3C, 0x0CBF604B6, 0x3B8F4BB3,
    0x0F744EB8E, 0x2802DD7D, 0x67434BBA, 0x0F744EB8E, 0x3119EC3C,
    0x2802DD7D, 0x0F744EB8E, 0x7E587AFB, 0x813416E7, 0x0F744EB8E,
    0x0CBF604B6, 0x7E587AFB, 0x0CBF604B6, 0x3119EC3C, 0x10A21870,
    0x813416E7, 0x3A1EE510, 0x46F8BFF6, 0x50F6ADAE,
]



dword_620 = [x & 0xFFFFFFFF for x in dword_620]

def crc32_update(crc, byte):
    v4 = crc ^ byte
    for _ in range(8):
        if v4 & 1:
            v4 = (v4 >> 1) ^ 0xEDB88320
        else:
            v4 >>= 1
    return v4 & 0xFFFFFFFF

def hash_byte(a1, a2):
    v3 = crc32_update(0xFFFFFFFF, a1)
    return (~crc32_update(v3, a2)) & 0xFFFFFFFF

import string

def brute_force_flag():
    flag_chars = []
    max_len = len(dword_620)
    for i in range(max_len):
        for c in string.printable:
            if hash_byte(ord(c), 0x5A) == dword_620[i]:
                flag_chars.append(c)
                print(f"Found char at position {i}: {c}")
                break
        else:
            print(f"No match found for position {i}")
            flag_chars.append('?')  # unknown char
    return "".join(flag_chars)

flag = brute_force_flag()
print("Flag:", flag)
