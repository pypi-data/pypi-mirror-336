import random
from sympy import jacobi_symbol

def solovay_strassen(n, k=5):
    """Perform the Solovay-Strassen primality test on a given number."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False

    for _ in range(k):
        a = random.randint(2, n - 1)
        j_symbol = jacobi_symbol(a, n) % n
        mod_exp = pow(a, (n - 1) // 2, n)
        if j_symbol == 0 or mod_exp != j_symbol:
            return False
    return True

if __name__ == "__main__":
    # Example Usage
    num = 101
    print(f"Solovay-Strassen: {num} is prime? {solovay_strassen(num)}")