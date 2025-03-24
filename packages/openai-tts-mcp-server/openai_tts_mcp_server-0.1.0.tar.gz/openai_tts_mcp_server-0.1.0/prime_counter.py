def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    
    return True

def count_primes(limit: int) -> int:
    """Count the number of prime numbers from 0 to limit (inclusive)."""
    count = 0
    for num in range(limit + 1):
        if is_prime(num):
            count += 1
    return count

def main():
    limit = 100
    prime_count = count_primes(limit)
    primes = [num for num in range(limit + 1) if is_prime(num)]
    
    print(f"Number of primes between 0 and {limit}: {prime_count}")
    print(f"Prime numbers: {primes}")

if __name__ == "__main__":
    main() 