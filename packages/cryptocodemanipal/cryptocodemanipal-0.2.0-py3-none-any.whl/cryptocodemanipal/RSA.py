from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generate RSA Key Pair
def generate_rsa_keys():
    key = RSA.generate(2048)  # Increased key size for better security
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Encrypt a message using RSA
def rsa_encrypt(message, public_key):
    try:
        key = RSA.import_key(public_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.encrypt(message.encode())
    except Exception as e:
        print("Encryption Error:", str(e))
        return None

# Decrypt a message using RSA
def rsa_decrypt(encrypted_message, private_key):
    try:
        key = RSA.import_key(private_key)
        cipher = PKCS1_OAEP.new(key)
        return cipher.decrypt(encrypted_message).decode()
    except Exception as e:
        print("Decryption Error:", str(e))
        return None

# Example Usage
if __name__ == "__main__":
    private_key, public_key = generate_rsa_keys()
    message = "Hello, RSA!"
    
    encrypted = rsa_encrypt(message, public_key)
    if encrypted:
        print("Encrypted:", encrypted.hex())  # Show as hex string

    decrypted = rsa_decrypt(encrypted, private_key)
    if decrypted:
        print("Decrypted Message:", decrypted)