# is_prime

A simple Python package to check if a number is prime.

## Installation

```bash
pip install is_prime_check
```

## Usage

```python
from is_prime import is_prime, get_primes

# Check if a single number is prime
print(is_prime(17))  # True
print(is_prime(4))   # False

# Get primes in a range
print(get_primes(10, 20))  # [11, 13, 17, 19]
```

## Features

- Check primality of integers
- Generate lists of prime numbers
- Efficient algorithm with O(sqrt(n)) time complexity

## License

MIT License
