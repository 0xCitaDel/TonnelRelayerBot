import binascii
import hashlib

from Crypto import Random
from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder


class AESCipher:
    """
    AESCipher provides encryption and decryption using AES with a passphrase.
    It uses an OpenSSL-compatible KDF (Key Derivation Function) similar to EVP_BytesToKey.
    """

    def __init__(self, passphrase, key_size=32, iv_size=16, hash_algorithm="md5"):
        """
        Initializes the AESCipher instance.

        :param passphrase: The password used to generate the encryption key.
        :param key_size: The size of the AES key in bytes (default: 32 for AES-256).
        :param iv_size: The size of the IV (Initialization Vector) in bytes (default: 16).
        :param hash_algorithm: The hash algorithm used for key derivation (default: MD5).
        """
        self.passphrase = passphrase
        self.key_size = key_size
        self.iv_size = iv_size
        self.hash_algorithm = hash_algorithm

    def _evp_kdf(self, salt):
        """
        OpenSSL-compatible Key Derivation Function (KDF).
        Converts a passphrase and salt into a cryptographic key and IV.

        :param salt: 8-byte salt.
        :return: (key, iv) tuple.
        """
        target_size = self.key_size + self.iv_size
        derived_bytes = b""
        prev_hash = b""

        # Generate key + IV using iterative hashing
        for _ in range(target_size // hashlib.new(self.hash_algorithm).digest_size + 1):
            hasher = hashlib.new(self.hash_algorithm)

            hasher.update(prev_hash)  # Hash previous output (if any)
            hasher.update(self.passphrase.encode())  # Hash the passphrase
            hasher.update(salt)  # Hash the salt

            prev_hash = hasher.digest()
            derived_bytes += prev_hash

        # Extract key and IV from derived bytes
        key = derived_bytes[: self.key_size]
        iv = derived_bytes[self.key_size : self.key_size + self.iv_size]

        return key, iv

    def encrypt(self, plaintext, salt=None):
        """
        Encrypts plaintext using AES-CBC.

        :param plaintext: The data to encrypt.
        :param salt: 8-byte salt (optional, generates one if None).
        :return: Base64-encoded encrypted string.
        """
        if salt is None:
            salt = Random.new().read(8)  # Generate a random 8-byte salt

        key, iv = self._evp_kdf(salt)  # Derive key and IV

        # Create AES cipher in CBC mode
        aes = AES.new(key, AES.MODE_CBC, iv)

        # Apply PKCS7 padding to plaintext
        encoder = PKCS7Encoder()
        padded_text = encoder.encode(plaintext)

        # Encrypt the padded text
        encrypted_text = aes.encrypt(padded_text.encode())

        # OpenSSL-compatible format: "Salted__" + salt + encrypted_data
        concat = b"Salted__" + salt + encrypted_text

        # Encode in Base64 for easy storage/transmission
        return binascii.b2a_base64(concat).rstrip().decode()

    def decrypt(self, encrypted_text):
        """
        Decrypts an AES-CBC encrypted Base64 string.

        :param encrypted_text: The encrypted data in Base64 format.
        :return: Decrypted plaintext.
        """
        encrypted_text_bytes = binascii.a2b_base64(encrypted_text)

        # Remove "Salted__" prefix
        encrypted_text_bytes = encrypted_text_bytes[8:]

        # Extract salt
        salt = encrypted_text_bytes[:8]
        encrypted_text_bytes = encrypted_text_bytes[8:]

        # Derive key and IV using the extracted salt
        key, iv = self._evp_kdf(salt)

        # Create AES cipher in CBC mode
        cipher = AES.new(key, AES.MODE_CBC, iv)

        # Decrypt the text
        decrypted_text = cipher.decrypt(encrypted_text_bytes)

        # Remove PKCS7 padding
        encoder = PKCS7Encoder()
        unpadded_text = encoder.decode(decrypted_text.decode())

        return unpadded_text


# 🔹 Example Usage
if __name__ == "__main__":
    passphrase = "yowtfisthispieceofshitiiit"
    plaintext = "U2FsdGVkX1++Lr+FGhr3RuN98iven6uP/PSqhtakyZ8="

    cipher = AESCipher(passphrase)

    # Decrypt data
    decrypted = cipher.decrypt(plaintext)
    print(f"🔓 Decrypted: {decrypted}\n")
