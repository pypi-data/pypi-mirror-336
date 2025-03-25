def jacobi(a, n):
    """Compute the Jacobi symbol (a/n)."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("n must be a positive odd integer")

    a = a % n
    result = 1

    while a:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result

        a, n = n, a  # Reciprocity
        if a % 4 == 3 and n % 4 == 3:
            result = -result

        a %= n

    return result if n == 1 else 0

if __name__ == "__main__":
    # Example Usage
    a = 100
    n = 201
    print(f"Jacobi({a}/{n}) =", jacobi(a, n))