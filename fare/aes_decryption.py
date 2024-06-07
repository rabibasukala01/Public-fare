from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import binascii

# Define your decryption function
def decrypt_data(hex_data):

    # Convert hex string to bytes
    binary_data = binascii.unhexlify(hex_data)

    # Define your key (must be 16, 24, or 32 bytes long for AES-128, AES-192, or AES-256 respectively)
    key = b'guesskeyifyoucan'  # Replace with AES key

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(binary_data) + decryptor.finalize()
    return decrypted_data.decode()



if __name__ == "__main__":
    # Assuming you have received the hex data as a string
    hex_data = "1F4CE9D13DE8AE47F9EA66248FE777BA"

    # Decrypt the data
    decrypted_text = decrypt_data(hex_data)

    print("Decrypted text:", decrypted_text[:10])
