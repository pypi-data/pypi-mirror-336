from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA Key Pair
def generate_rsa_keys():
    key = RSA.generate(1024)  # Smaller key size for simplicity
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Encrypt a message using RSA
def rsa_encrypt(message, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(message.encode())

# Decrypt a message using RSA
def rsa_decrypt(encrypted_message, private_key):
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.decrypt(encrypted_message).decode()

# Example Usage
private_key, public_key = generate_rsa_keys()
encrypted = rsa_encrypt("Hello, RSA!", public_key)
decrypted = rsa_decrypt(encrypted, private_key)
print("Decrypted Message:", decrypted)
