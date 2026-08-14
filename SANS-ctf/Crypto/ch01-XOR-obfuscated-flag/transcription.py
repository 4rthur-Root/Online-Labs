import binascii

def encrypt(input_string):
    result = ""
    key = [3, 19, 1337, 42, 9, 11, 56, 2, 72, 100, 81, 90, 11, 23, 84, 77, 192, 810, 999, 239, 74]
    phrase1 = "the quick fox jumps over the lazy dog"
    phrase2 = "lorem ipsum dolor sit amet consectetur adipiscing elit"

    for i in range(0, len(input_string)):
        char1 = phrase1[(key[i] * i) % len(phrase1)]
        char2 = phrase2[(key[i] * i) % len(phrase2)]
        xor1 = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(char1, char2))
        xor2 = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(xor1, input_string[i]))
        result += binascii.hexlify(xor2.encode()).decode()
    return result[::-1]

def decrypt(input_string):
    # Decryption algorithm
    key = [3, 19, 1337, 42, 9, 11, 56, 2, 72, 100, 81, 90, 11, 23, 84, 77, 192, 810, 999, 239, 74]
    phrase1 = "the quick fox jumps over the lazy dog"
    phrase2 = "lorem ipsum dolor sit amet consectetur adipiscing elit"
    
    # Reverse the encryption: reverse string, decode hex, then reverse XOR
    reversed_enc = input_string[::-1]
    decoded = []
    for i in range(0, len(reversed_enc), 2):
        hex_char = reversed_enc[i:i+2]
        decoded.append(binascii.unhexlify(hex_char).decode())
    
    result = ""
    for i, char in enumerate(decoded):
        char1 = phrase1[(key[i] * i) % len(phrase1)]
        char2 = phrase2[(key[i] * i) % len(phrase2)]
        xor1 = chr(ord(char1) ^ ord(char2))
        input_char = chr(ord(xor1) ^ ord(char))
        result += input_char
    
    return result

user_input = input("> ")
print(encrypt(user_input))
