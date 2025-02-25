from Logger import logging
from File_path import secret_key_path, activation_key_path
from cryptography.fernet import Fernet
import json

def encrypt_key(key_code):
    encryption_key = load_encryption_key()
    if encryption_key:
        fernet = Fernet(encryption_key)
        encrypted_key = fernet.encrypt(key_code.encode())
        logging.info(f"Encrypted key_code '{key_code}'")
        return encrypted_key
    return None



def load_encryption_key():
    if secret_key_path.exists() and secret_key_path.stat().st_size > 0:
        with open(secret_key_path, "rb") as key_file:
            logging.info("Secret_key_path exsist and content is bigger then 0 returning key_file.read")
            return key_file.read()
    else:
        logging.info("Encryption key not found. Generating a new one.")
        key = Fernet.generate_key()
        with open(secret_key_path, "wb") as key_file:
            key_file.write(key)
        return key



def save_key(encrypted_key):
    key_data = {"key_code": encrypted_key.decode()}  # Assuming you want to store the encrypted key as a string
    with open(activation_key_path, "w") as file:
        json.dump(key_data, file)
    logging.info("Saved encrypted key to activation_key.json")