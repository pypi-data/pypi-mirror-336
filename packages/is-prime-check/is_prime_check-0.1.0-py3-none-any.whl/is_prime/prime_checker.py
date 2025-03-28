def is_prime(n):
    """
    Check if a given number is prime.

    Args:
        n (int): The number to check for primality.

    Returns:
        bool: True if the number is prime, False otherwise.

    Raises:
        ValueError: If the input is not a positive integer.
    """
    # Validate input
    if not isinstance(n, int):
        raise ValueError("Input must be an integer")

    # Handle edge cases
    if n <= 1:
        return False

    # Optimization: check divisibility up to square root
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False

    return True


def get_primes(start, end):
    """
    Generate a list of prime numbers within a given range.

    Args:
        start (int): The start of the range (inclusive).
        end (int): The end of the range (inclusive).

    Returns:
        list: A list of prime numbers in the given range.
    """
    return [num for num in range(start, end + 1) if is_prime(num)]
