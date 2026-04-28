from cryptography.fernet import Fernet
import os
from PIL import Image
from io import BytesIO

# Define the path to the keylogger folder in the backend directory
KEYLOGGER_FOLDER = os.path.join("keylogger")
KEY_FILE = os.path.join(KEYLOGGER_FOLDER, "keystroke_key.key")

# Global cipher suite
cipher_suite = None

# Create the keylogger folder if it doesn't exist
if not os.path.exists(KEYLOGGER_FOLDER):
    os.makedirs(KEYLOGGER_FOLDER)
    print(f"Created keylogger folder at: {os.path.abspath(KEYLOGGER_FOLDER)}")

def load_key(key_file=KEY_FILE):
    """
    Loads the encryption key from a file. If the file doesn't exist, it generates a new key.
    """
    if not os.path.exists(key_file):
        return generate_and_save_key(key_file)
    with open(key_file, "rb") as f:
        return f.read()

def generate_and_save_key(key_file=KEY_FILE):
    """
    Generates a new encryption key and saves it to a file.
    """
    key = Fernet.generate_key()  # This returns bytes
    with open(key_file, "wb") as f:
        f.write(key)
    print(f"Encryption key saved to: {os.path.abspath(key_file)}")
    return key

def set_decryption_key(key):
    """
    Sets the decryption key dynamically.
    """
    global cipher_suite
    cipher_suite = Fernet(key)  # No need to encode, as key is already in bytes

# Load the key automatically when the module is imported
key = load_key()
set_decryption_key(key)

def encrypt_data(data):
    """
    Encrypts the given data using the encryption key.
    """
    if not cipher_suite:
        raise ValueError("Decryption key not set.")
    encrypted_data = cipher_suite.encrypt(data.encode())  # Encodes the input data
    return encrypted_data.decode("utf-8")  # Decodes the encrypted data to a string

def decrypt_data(encrypted_data):
    """
    Decrypts the given encrypted data using the encryption key.
    """
    if not cipher_suite:
        raise ValueError("Decryption key not set.")
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode())  # Encodes the input data
        return decrypted_data.decode("utf-8")  # Decodes the decrypted data to a string
    except Exception as e:
        return f"[Decryption Error: {str(e)}]"

def encrypt_image(image_path, output_path=None):
    """
    Encrypts an image file and saves it with .enc extension
    """
    if not cipher_suite:
        raise ValueError("Decryption key not set.")
    
    if not output_path:
        output_path = image_path + '.enc'
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    encrypted_data = cipher_suite.encrypt(image_data)
    
    with open(output_path, 'wb') as f:
        f.write(encrypted_data)
    
    # Remove original unencrypted file
    os.remove(image_path)
    
    return output_path

def decrypt_image(encrypted_path, output_path=None):
    """
    Decrypts an encrypted image file and returns the image data
    """
    if not cipher_suite:
        raise ValueError("Decryption key not set.")
    
    if not output_path:
        output_path = encrypted_path.replace('.enc', '')
    
    with open(encrypted_path, 'rb') as f:
        encrypted_data = f.read()
    
    try:
        decrypted_data = cipher_suite.decrypt(encrypted_data)
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")
    
    # For in-memory use (dashboard display)
    if output_path == ':memory:':
        return BytesIO(decrypted_data)
    
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)
    
    return output_path

def get_image_size(image_path):
    """
    Returns the dimensions of an image file
    """
    if image_path.endswith('.enc'):
        # For encrypted images, decrypt to memory first
        image_data = decrypt_image(image_path, ':memory:')
        with Image.open(image_data) as img:
            return img.size
    else:
        with Image.open(image_path) as img:
            return img.size