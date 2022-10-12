try:
    from functions import *
except:
    from encryption.functions import *
try:
    from encryption import *
except:
    from encryption.encryption import *
try:
    from config import *
except:
    from encryption.config import *

# generate_and_save_keys()

private_key = load_private_key()
public_key = load_public_key()

private_key_objective, public_key_objective = generate_keys()

encryptor = Encryption(private_key, public_key)
msg = "HOLAAA, ESTO ES UN TEST"

encrypted_msg = encryptor.encrypt(msg, public_key_objective)
print(encrypted_msg)

decryptor = Encryption(private_key_objective, public_key_objective)
decrypted_msg = decryptor.decrypt(encrypted_msg, public_key)
print(decrypted_msg)