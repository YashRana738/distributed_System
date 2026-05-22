import random
import math
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True
def generate_prime(start=100, end=300):
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num
def generate_keys():
    p = generate_prime()
    q = generate_prime()

    while p == q:
        q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)

    d = pow(e, -1, phi)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key
def encrypt(message, public_key):
    e, n = public_key
    encrypted = [pow(ord(char), e, n) for char in message]
    return encrypted
def decrypt(ciphertext, private_key):
    d, n = private_key
    decrypted = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return decrypted

public_key, private_key = generate_keys()

print("Public Key:", public_key)
print("Private Key:", private_key)

message = "HELLO DISTRIBUTED SYSTEM"
ciphertext = encrypt(message, public_key)
print("\nEncrypted Message:", ciphertext)

decrypted_message = decrypt(ciphertext, private_key)
print("\nDecrypted Message:", decrypted_message)
