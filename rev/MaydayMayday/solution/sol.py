def phonetic_decode(s):
    # Reverse ROT13 (same as forward ROT13)
    result = []
    for ch in s:
        if 'a' <= ch <= 'z':
            result.append(chr((ord(ch) - ord('a') + 13) % 26 + ord('a')))
        elif 'A' <= ch <= 'Z':
            result.append(chr((ord(ch) - ord('A') + 13) % 26 + ord('A')))
        else:
            result.append(ch)
    return ''.join(result)


def aviation_decrypt(data, frequency):
    return ''.join(chr(ord(c) ^ frequency) for c in data)


def main():
    # #~&# &\'v:m#\" $r:t&n\' ::
    authorized_route = [35,126,38,35,32,38,39,118,58,109,35,34,32,36,114,58,116,38,110,39,32,58,58]

    print("Original bytes:")
    print(" ".join(chr(b) for b in authorized_route))

    # Step 1: Reverse XOR with 23 (0x17)
    xor_reversed = ''.join(chr(b ^ 23) for b in authorized_route)
    print("\nAfter XOR reversal:")
    print(" ".join(f"{ord(c)}('{c}')" for c in xor_reversed))

    # Step 2: Reverse ROT13
    rot13_reversed = phonetic_decode(xor_reversed)
    print("\nAfter ROT13 reversal:")
    print(" ".join(f"{ord(c)}('{c}')" for c in rot13_reversed))

    print(f"\nDecoded middle part: '{rot13_reversed}'")
    print(f"Full flag: METACTF{{{rot13_reversed}}}")

if __name__ == "__main__":
    main()
