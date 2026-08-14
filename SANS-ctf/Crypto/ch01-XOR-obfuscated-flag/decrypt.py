import binascii

# The encrypted flag from flag.txt
encrypted_flag = "7792c3732707226742f346b62702d77747c76216"

# Reverse the string (as done in the encryption)
reversed_flag = encrypted_flag[::-1]

# The key and phrases from the encryption function
key = [3, 19, 1337, 42, 9, 11, 56, 2, 72, 100, 81, 90, 11, 23, 84, 77, 192, 810, 999, 239, 74]
phrase1 = "the quick fox jumps over the lazy dog"
phrase2 = "lorem ipsum dolor sit amet consectetur adipiscing elit"

# Decode each 2-character hex pair
decoded = []
for i in range(0, len(reversed_flag), 2):
    hex_char = reversed_flag[i:i+2]
    decoded.append(binascii.unhexlify(hex_char).decode())

print("Decoded hex values:", decoded)

# Now we need to reverse the XOR operations
# xor2 = xor1 XOR input_char
# Therefore: input_char = xor1 XOR xor2

result = ""
for i, char in enumerate(decoded):
    # Get the derived characters from phrases
    char1 = phrase1[(key[i] * i) % len(phrase1)]
    char2 = phrase2[(key[i] * i) % len(phrase2)]
    
    # xor1 = char1 XOR char2
    xor1 = chr(ord(char1) ^ ord(char2))
    
    # input_char = xor1 XOR xor2 (where char is xor2)
    input_char = chr(ord(xor1) ^ ord(char))
    result += input_char

print("Decrypted flag:", result)

