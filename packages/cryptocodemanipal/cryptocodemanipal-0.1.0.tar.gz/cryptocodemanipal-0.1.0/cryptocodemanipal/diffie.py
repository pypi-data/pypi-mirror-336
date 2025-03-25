import random

# Step 1: Public Parameters (agreed upon by both parties)
p = 71  # Prime number
g = 5   # Generator

# Step 2: Alice chooses a private key and computes a public key
alice_private = random.randint(2, p - 2)
alice_public = pow(g, alice_private, p)

# Step 3: Bob chooses a private key and computes a public key
bob_private = random.randint(2, p - 2)
bob_public = pow(g, bob_private, p)

# Step 4: Exchange public keys and compute the shared secret
alice_shared_secret = pow(bob_public, alice_private, p)
bob_shared_secret = pow(alice_public, bob_private, p)

# The shared secret should be the same for both
print("Alice's Shared Secret:", alice_shared_secret)
print("Bob's Shared Secret:", bob_shared_secret)