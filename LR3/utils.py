from pyDes import des, PAD_PKCS5
import base64

def _get_cipher(key: str) -> des:
    return des(key[:8], padmode=PAD_PKCS5)

def encrypt(text: str, key: str) -> str:
    cipher = _get_cipher(key)
    encrypted_text = cipher.encrypt(text)
    return base64.b64encode(encrypted_text).decode('utf-8')

def decrypt(encrypted_text_base64: str, key: str) -> str:
    cipher = _get_cipher(key)
    encrypted_text = base64.b64decode(encrypted_text_base64)
    return cipher.decrypt(encrypted_text).decode('utf-8')
