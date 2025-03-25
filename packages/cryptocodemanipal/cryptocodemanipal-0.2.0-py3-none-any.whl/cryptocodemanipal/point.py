from sympy import mod_inverse

# Define the elliptic curve parameters (y^2 = x^3 + ax + b over a finite field p)
a = 2
b = 3
p = 97  # Prime number for finite field

# Point Addition
def point_addition(P, Q):
    """Perform elliptic curve point addition."""
    if P == Q:
        return point_doubling(P)

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == y2:
        return point_doubling(P)

    m = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

# Point Doubling
def point_doubling(P):
    """Perform elliptic curve point doubling."""
    x1, y1 = P

    if y1 == 0:
        return None  # Point at infinity

    m = ((3 * x1**2 + a) * mod_inverse(2 * y1, p)) % p
    x3 = (m**2 - 2 * x1) % p
    y3 = (m * (x1 - x3) - y1) % p

    return (x3, y3)

if __name__ == "__main__":
    # Example Usage
    P = (3, 6)
    Q = (10, 20)

    # Point Addition
    R = point_addition(P, Q)
    print("P + Q =", R)

    # Point Doubling
    D = point_doubling(P)
    print("2P =", D)