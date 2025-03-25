def rsa_key_generation():
    # Step 1: Choose two distinct prime numbers (in real use, these are large primes)
    p = 61
    q = 53

    # Step 2: Compute n (modulus)
    n = p * q

    # Step 3: Compute Euler's totient function (phi)
    phi = (p - 1) * (q - 1)

    # Step 4: Choose e (public exponent) that is coprime with phi
    e = 17  # Commonly used values include 3, 17, 65537

    # Step 5: Compute d (private exponent) as the modular inverse of e mod phi
    def mod_inverse(a, m):
        # Extended Euclidean Algorithm to find modular inverse
        g, x, y = extended_gcd(a, m)
        if g != 1:
            return None  # Inverse doesn't exist
        else:
            return x % m

    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = extended_gcd(b % a, a)
            return (g, x - (b // a) * y, y)

    d = mod_inverse(e, phi)

    return (e, n), (d, n)

def rsa_encrypt(message, public_key):
    e, n = public_key
    # Encrypt message: c = message^e mod n
    ciphertext = pow(message, e, n)
    return ciphertext

def rsa_decrypt(ciphertext, private_key):
    d, n = private_key
    # Decrypt ciphertext: m = ciphertext^d mod n
    plaintext = pow(ciphertext, d, n)
    return plaintext

# Generate keys
public_key, private_key = rsa_key_generation()
print("Public Key (e, n):", public_key)
print("Private Key (d, n):", private_key)

# Example message (must be an integer less than n)
message = 65
print("\nOriginal Message:", message)

# Encryption
encrypted_msg = rsa_encrypt(message, public_key)
print("Encrypted Message:", encrypted_msg)

# Decryption
decrypted_msg = rsa_decrypt(encrypted_msg, private_key)
print("Decrypted Message:", decrypted_msg)