from base64 import b64encode, b64decode
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Protocol.KDF import PBKDF2
import json

from password_manager.models import PrivateKey


def derive_key(password, salt):
    kdf = PBKDF2(password, salt, 64, 1000)
    key = kdf[:32]
    return key


def encrypt(user_master_password, social_password, private_salt):
    if type(user_master_password) is bytes:

        salt = private_salt
        private_key = user_master_password

    else:
        salt = get_random_bytes(AES.block_size)
        private_key = derive_key(user_master_password, salt)

    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(
        bytes(social_password, "utf-8")
    )

    dictionary = {
        'cipher_text': b64encode(cipher_text).decode('utf-8'),
        'salt': b64encode(salt).decode('utf-8'),
        'nonce': b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': b64encode(tag).decode('utf-8')
    }

    return json.dumps(dictionary)


def decrypt(encrypted_dict, user_master_password):
    salt = b64decode(encrypted_dict["salt"])
    cipher_text = b64decode(encrypted_dict["cipher_text"])
    nonce = b64decode(encrypted_dict["nonce"])
    tag = b64decode(encrypted_dict["tag"])

    private_key = derive_key(user_master_password, salt)

    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)

    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    
    return decrypted


def verify_master_password(encrypted_dict, master_password):
    try:
        decrypt(encrypted_dict, master_password)
        return True
    except:
        return False
