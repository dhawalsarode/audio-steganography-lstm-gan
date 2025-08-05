# backend/utils/aes_utils.py

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import base64

BLOCK_SIZE = 16  # AES block size in bytes

def pad(text):
    pad_len = BLOCK_SIZE - len(text) % BLOCK_SIZE
    return text + chr(pad_len) * pad_len

def unpad(text):
    pad_len = ord(text[-1])
    return text[:-pad_len]

def derive_key(password: str) -> bytes:
    """Derives a 256-bit AES key from a string password."""
    return hashlib.sha256(password.encode()).digest()

def encrypt_message(message: str, password: str) -> str:
    """Encrypts a message using AES-CBC and returns base64 string."""
    key = derive_key(password)
    iv = get_random_bytes(BLOCK_SIZE)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded = pad(message)
    encrypted_bytes = cipher.encrypt(padded.encode())

    # Combine IV + ciphertext and base64 encode
    encrypted_data = base64.b64encode(iv + encrypted_bytes).decode()
    return encrypted_data

def decrypt_message(encrypted_data: str, password: str) -> str:
    """Decrypts a base64-encoded AES-CBC encrypted string."""
    key = derive_key(password)
    raw = base64.b64decode(encrypted_data)
    iv = raw[:BLOCK_SIZE]
    encrypted_bytes = raw[BLOCK_SIZE:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted_bytes).decode()
    return unpad(decrypted)
