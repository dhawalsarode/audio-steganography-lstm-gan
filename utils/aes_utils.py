import base64
import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

BLOCK_SIZE = 16
SALT_SIZE = 16
KEY_SIZE = 32
ITERATIONS = 100000

def encrypt_message(message: str, password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode("utf-8"))
    data = salt + cipher.nonce + tag + ciphertext
    return base64.b64encode(data).decode("utf-8")

def decrypt_message(encrypted_b64: str, password: str) -> str:
    try:
        raw = base64.b64decode(encrypted_b64)
        salt = raw[:SALT_SIZE]
        nonce = raw[SALT_SIZE:SALT_SIZE+BLOCK_SIZE]
        tag = raw[SALT_SIZE+BLOCK_SIZE:SALT_SIZE+BLOCK_SIZE+16]
        ciphertext = raw[SALT_SIZE+BLOCK_SIZE+16:]
        key = PBKDF2(password, salt, dkLen=KEY_SIZE, count=ITERATIONS)
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        message = cipher.decrypt_and_verify(ciphertext, tag)
        return message.decode("utf-8")
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
