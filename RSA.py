import random
from math import gcd
import os

# Prime check
def is_prime(n):
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

# Modular inverse
def modinv(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

# Key generation
def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be the same")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(2, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)
    d = modinv(e, phi)
    return ((e, n), (d, n))

# Encrypt message
def encrypt(pk, plaintext):
    key, n = pk
    return [pow(ord(char), key, n) for char in plaintext]

# Decrypt message
def decrypt(pk, ciphertext):
    key, n = pk
    return ''.join([chr(pow(char, key, n)) for char in ciphertext])

# Read file or input
def get_message():
    choice = input("Choose input method:\n1. Type/Paste message\n2. Upload .txt file\nEnter 1 or 2: ")
    if choice == "1":
        return input("\nEnter your message:\n")
    elif choice == "2":
        filepath = input("Enter path to the .txt file: ")
        if not os.path.isfile(filepath) or not filepath.endswith('.txt'):
            raise FileNotFoundError("Invalid file. Make sure it's a .txt file and the path is correct.")
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        raise ValueError("Invalid choice. Please enter 1 or 2.")

# Main program
def main():
    print("🔐 RSA Encryption Software 🔐")
    try:
        p = int(input("Enter a prime number (p): "))
        q = int(input("Enter another prime number (q): "))
        public_key, private_key = generate_keypair(p, q)
        
        print("\n✅ Keys generated:")
        print("Public Key (e, n):", public_key)
        print("Private Key (d, n):", private_key)

        message = get_message()

        encrypted = encrypt(public_key, message)
        print("\n🔒 Encrypted Message:")
        print(encrypted)

        decrypted = decrypt(private_key, encrypted)
        print("\n🔓 Decrypted Message:")
        print(decrypted)

    except ValueError as ve:
        print("❌ Value Error:", ve)
    except FileNotFoundError as fnfe:
        print("❌ File Error:", fnfe)
    except Exception as e:
        print("❌ Unexpected Error:", e)

if __name__ == "__main__":
    main()
