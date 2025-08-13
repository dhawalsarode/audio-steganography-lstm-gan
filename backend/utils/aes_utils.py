# backend/utils/aes_utils.py

import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

BLOCK_SIZE = 16
KEY_SIZE = 32
SALT_SIZE = 16

def pad(text):
    pad_len = BLOCK_SIZE - len(text) % BLOCK_SIZE
    return text + chr(pad_len) * pad_len

def unpad(text):
    pad_len = ord(text[-1])
    return text[:-pad_len]

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, dkLen=KEY_SIZE)

def encrypt_message(message: str, password: str) -> str:
    salt = get_random_bytes(SALT_SIZE)
    key = derive_key(password, salt)
    iv = get_random_bytes(BLOCK_SIZE)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(message)
    encrypted_bytes = cipher.encrypt(padded.encode())

    # Combine salt + IV + ciphertext
    encrypted_data = base64.b64encode(salt + iv + encrypted_bytes).decode()
    return encrypted_data

def decrypt_message(encrypted_data: str, password: str) -> str:
    raw = base64.b64decode(encrypted_data)
    salt = raw[:SALT_SIZE]
    iv = raw[SALT_SIZE:SALT_SIZE+BLOCK_SIZE]
    ciphertext = raw[SALT_SIZE+BLOCK_SIZE:]

    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext).decode()
    return unpad(decrypted)
