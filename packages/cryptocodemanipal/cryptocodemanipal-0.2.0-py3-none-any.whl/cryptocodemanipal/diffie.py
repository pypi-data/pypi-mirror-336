import random

# Step 1: Public Parameters (agreed upon by both parties)
p = 71  # Prime number
g = 5   # Generator

def generate_private_public():
    """Generate a private key and corresponding public key."""
    private_key = random.randint(2, p - 2)
    public_key = pow(g, private_key, p)
    return private_key, public_key

def compute_shared_secret(private_key, other_public_key):
    """Compute the shared secret using own private key and the other party's public key."""
    return pow(other_public_key, private_key, p)

if __name__ == "__main__":
    # Step 2: Alice generates her keys
    alice_private, alice_public = generate_private_public()

    # Step 3: Bob generates his keys
    bob_private, bob_public = generate_private_public()

    # Step 4: Compute shared secret
    alice_shared_secret = compute_shared_secret(alice_private, bob_public)
    bob_shared_secret = compute_shared_secret(bob_private, alice_public)

    # Output results
    print("Alice's Shared Secret:", alice_shared_secret)
    print("Bob's Shared Secret:", bob_shared_secret)

    # Check if they are equal
    assert alice_shared_secret == bob_shared_secret, "Error: Shared secrets do not match!"