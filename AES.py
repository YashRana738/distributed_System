from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

def generate_aes_key():
    return get_random_bytes(16)

def aes_encrypt(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv, ct_bytes

def aes_decrypt(iv, ciphertext, key):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return pt.decode()

if __name__ == "__main__":
    aes_key = generate_aes_key()

    iv, aes_cipher = aes_encrypt("SECURE MESSAGE USING AES", aes_key)
    aes_plain = aes_decrypt(iv, aes_cipher, aes_key)

    print("AES Decrypted:", aes_plain)
