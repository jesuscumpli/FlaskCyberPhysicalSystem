from Crypto.Util.Padding import pad, unpad
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import Crypto.Util.number
from hashlib import sha512
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256

import os
import json
import base64

try:
    from config import *
except:
    from encryption.config import *

class Encryption():

    def __init__(self, my_private_key, my_public_key):
        self.private_key = my_private_key
        self.public_key = my_public_key

    def encrypt(self, msg, public_key_objective):
        # 0. Encode message
        msg_bytes = msg.encode("ISO-8859-1")

        # 1. Message Bytes to Base64
        msg_b64 = base64.b64encode(msg_bytes)
        # Padding
        msg_b64 = pad(msg_b64, BS)

        # 2. Generate session key
        secret_key = os.urandom(16)

        # 3. Encrypt message with secret key
        iv = Random.new().read(AES.block_size)
        aes_engine = AES.new(secret_key, AES.MODE_CBC, iv)
        encrypted_msg = aes_engine.encrypt(msg_b64)
        # Adjuntamos iv en claro al inicio del fichero encriptado (16 primeros bytes)
        encrypted_msg = (iv + encrypted_msg)

        # 4. Encrypt secret key with public key
        encryptor = PKCS1_OAEP.new(public_key_objective)
        encrypted_secret_key = encryptor.encrypt(secret_key)

        # 5. Create Signature of Encrypted File
        # hash = int.from_bytes(sha512(encrypted_msg).digest(), byteorder='big')
        # signature = hex(pow(hash, self.private_key.d, self.private_key.n))
        hash = SHA256.new(encrypted_msg)
        signer = PKCS115_SigScheme(self.private_key)
        signature = signer.sign(hash)

        # 6. Message: JSON Data
        json_data = {"key": encrypted_secret_key.decode("ISO-8859-1"), "msg": encrypted_msg.decode("ISO-8859-1"),
                     "signature": signature.decode("ISO-8859-1")}
        json_data_dumps = json.dumps(json_data) # dict to str
        json_data_dumps_encoded = json_data_dumps.encode("ISO-8859-1") # str to bytes

        # 7. Base64
        b64_data = base64.b64encode(json_data_dumps_encoded)

        return b64_data

    def decrypt(self, b64_data, public_key_origen):

        # 1. From Base64
        json_data_dumps_encoded = base64.b64decode(b64_data)

        # 2. JSON Data
        json_data_dumps = json_data_dumps_encoded.decode("ISO-8859-1")
        json_data = json.loads(json_data_dumps)

        # 3. Get Data
        encrypted_secret_key = json_data["key"].encode("ISO-8859-1")
        encrypted_msg = json_data["msg"].encode("ISO-8859-1")
        signature = json_data["signature"].encode("ISO-8859-1")

        # 4. Verify Hash
        # hash = int.from_bytes(sha512(encrypted_msg).digest(), byteorder='big')
        # signature_to_verify = hex(pow(hash, public_key_origen.e, public_key_origen.n))
        hash = SHA256.new(encrypted_msg)
        verifier = PKCS115_SigScheme(public_key_origen)
        try:
            verifier.verify(hash, signature)
        except:
            raise Exception("Error decrypting message: Signature incorrect!")

        # 5. Decrypt secret key
        encryptor = PKCS1_OAEP.new(self.private_key)
        secret_key = encryptor.decrypt(encrypted_secret_key)

        # 6. Decrypt message
        iv = encrypted_msg[:16]
        encrypted_msg = encrypted_msg[16:]
        aes_engine = AES.new(secret_key, AES.MODE_CBC, iv)
        msg_b64 = aes_engine.decrypt(encrypted_msg)
        # Unpadding
        msg_b64 = unpad(msg_b64, BS)

        # 7. Message Base64 to Message
        msg_bytes = base64.b64decode(msg_b64)
        msg = msg_bytes.decode("ISO-8859-1")

        return msg

