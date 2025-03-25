import random
from sympy import isprime, mod_inverse

# Generate large prime number for the modulus
def generate_large_prime(start=1000, end=5000):
    """Generate a large prime number within a given range."""
    while True:
        p = random.randint(start, end)
        if isprime(p):
            return p

# Generate keys for ElGamal encryption
def generate_elgamal_keys():
    """Generate public and private keys for ElGamal encryption."""
    p = generate_large_prime()
    g = random.randint(2, p - 1)  # Generator
    x = random.randint(2, p - 2)  # Private key
    y = pow(g, x, p)  # Public key
    return (p, g, y), x  # (Public Key), Private Key

# Encrypt message using ElGamal
def elgamal_encrypt(message, public_key):
    """Encrypt a message using ElGamal encryption."""
    p, g, y = public_key
    k = random.randint(2, p - 2)  # Random ephemeral key
    c1 = pow(g, k, p)
    c2 = (message * pow(y, k, p)) % p
    return c1, c2

# Decrypt message using ElGamal
def elgamal_decrypt(ciphertext, private_key, p):
    """Decrypt an ElGamal encrypted message."""
    c1, c2 = ciphertext
    s = pow(c1, private_key, p)  # Compute shared secret
    s_inv = mod_inverse(s, p)  # Compute modular inverse
    message = (c2 * s_inv) % p
    return message

if __name__ == "__main__":
    # Example Usage
    public_key, private_key = generate_elgamal_keys()
    message = 1234  # Message should be an integer

    ciphertext = elgamal_encrypt(message, public_key)
    decrypted_message = elgamal_decrypt(ciphertext, private_key, public_key[0])

    print("Original Message:", message)
    print("Ciphertext:", ciphertext)
    print("Decrypted Message:", decrypted_message)