from tinyec import registry
import secrets

# Get the elliptic curve
ecc_curve = registry.get_curve("secp192r1")

def generate_ecc_keys():
    """Generate a private and public key pair for ECC."""
    private_key = secrets.randbelow(ecc_curve.field.n)
    public_key = private_key * ecc_curve.g
    return private_key, public_key

def ecc_encrypt(message, public_key):
    """Encrypt a message using ECC (Elliptic Curve Diffie-Hellman)."""
    ephemeral_key = secrets.randbelow(ecc_curve.field.n)
    shared_secret = ephemeral_key * public_key
    encrypted_message = (shared_secret.x, message.encode())
    return ephemeral_key * ecc_curve.g, encrypted_message

def ecc_decrypt(encrypted_message, private_key):
    """Decrypt a message using ECC."""
    shared_secret = private_key * encrypted_message[0]
    decrypted_message = encrypted_message[1][1].decode()
    return decrypted_message

if __name__ == "__main__":
    # Example Usage
    private_key, public_key = generate_ecc_keys()
    
    message = "Hello, ECC!"
    ciphertext = ecc_encrypt(message, public_key)
    decrypted_message = ecc_decrypt(ciphertext, private_key)

    print("Decrypted Message:", decrypted_message)