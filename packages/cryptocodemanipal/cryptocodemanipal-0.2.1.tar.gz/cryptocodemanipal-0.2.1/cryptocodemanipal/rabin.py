from sympy import mod_inverse, isprime
from random import randint

# Generate Rabin Cryptosystem Keys (p and q must be 3 mod 4)
def generate_rabin_keys():
    """Generate Rabin cryptosystem keys where p and q are primes congruent to 3 mod 4."""
    while True:
        p, q = randint(1000, 5000), randint(1000, 5000)
        if isprime(p) and isprime(q) and p % 4 == 3 and q % 4 == 3:
            break
    return p, q, p * q

# Encrypt a message using Rabin Cryptosystem
def rabin_encrypt(message, n):
    """Encrypt a message using the Rabin cryptosystem."""
    m = int.from_bytes(message.encode(), 'big')
    return (m * m) % n

# Decrypt a message using Rabin Cryptosystem
def rabin_decrypt(ciphertext, p, q):
    """Decrypt a message using the Rabin cryptosystem."""
    n = p * q
    mp, mq = pow(ciphertext, (p + 1) // 4, p), pow(ciphertext, (q + 1) // 4, q)
    yp, yq = mod_inverse(p, q), mod_inverse(q, p)
    r1 = (yp * p * mq + yq * q * mp) % n
    r2 = n - r1
    return r1.to_bytes((r1.bit_length() + 7) // 8, 'big').decode(errors='ignore')

if __name__ == "__main__":
    # Example Usage
    p, q, n = generate_rabin_keys()
    ciphertext = rabin_encrypt("Hello", n)
    decrypted = rabin_decrypt(ciphertext, p, q)
    print("Decrypted Message:", decrypted)