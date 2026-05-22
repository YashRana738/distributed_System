from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def generate_des_key():
    return get_random_bytes(8)

def des_encrypt(message, key):
    cipher = DES.new(key, DES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), DES.block_size))
    return cipher.iv, ct_bytes

def des_decrypt(iv, ciphertext, key):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ciphertext), DES.block_size)
    return pt.decode()

des_key = generate_des_key()

iv, des_cipher = des_encrypt("HELLO DISTRIBUTED SYSTEM", des_key)
des_plain = des_decrypt(iv, des_cipher, des_key)

print("DES Decrypted:", des_plain)
