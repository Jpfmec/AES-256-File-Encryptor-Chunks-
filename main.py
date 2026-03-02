import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend

CHUNK_SIZE = 64 * 1024

def derive_key(password: str, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt_bytes(key: bytes, plaintext: bytes, nonce: bytes):
    aesgcm = AESGCM(key)
    return aesgcm.encrypt(nonce, plaintext, None)

def decrypt_bytes(key: bytes, ciphertext: bytes, nonce: bytes):
    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, None)

def encrypt_file(file_path: str):
    if not os.path.isfile(file_path):
        print("File not found!")
        return
    password = base64.urlsafe_b64encode(os.urandom(32)).decode()
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt)
    encrypted_file_path = file_path + ".enc"
    if os.path.exists(encrypted_file_path):
        choice = input(f"{encrypted_file_path} The file is already encripted. Override? (s/n): ").lower()
        if choice != 's':
            print("Operation cancelled.")
            return
    with open(file_path, "rb") as f_in, open(encrypted_file_path, "wb") as f_out:
        f_out.write(salt + nonce)
        while chunk := f_in.read(CHUNK_SIZE):
            encrypted_chunk = encrypt_bytes(key, chunk, nonce)
            f_out.write(len(encrypted_chunk).to_bytes(4, 'big'))
            f_out.write(encrypted_chunk)
    print(f"\nEncripted folder: {encrypted_file_path}")
    print(f"Code to decript: {password}")
    return password, encrypted_file_path

def decrypt_file(encrypted_file_path: str, password: str, output_path: str = None):
    if not os.path.isfile(encrypted_file_path):
        print("File not found!")
        return
    with open(encrypted_file_path, "rb") as f_in:
        salt = f_in.read(16)
        nonce = f_in.read(12)
        key = derive_key(password, salt)
        if output_path is None:
            output_path = encrypted_file_path.replace(".enc", ".dec")
        if os.path.exists(output_path):
            choice = input(f"{output_path} The file is already encripted. Override? (s/n): ").lower()
            if choice != 's':
                print("Operation cancelled.")
                return
        with open(output_path, "wb") as f_out:
            while True:
                size_bytes = f_in.read(4)
                if not size_bytes:
                    break
                chunk_size = int.from_bytes(size_bytes, 'big')
                encrypted_chunk = f_in.read(chunk_size)
                decrypted_chunk = decrypt_bytes(key, encrypted_chunk, nonce)
                f_out.write(decrypted_chunk)
    print(f"\nFile decripted: {output_path}")
    return output_path

def main():
    print("===== AES-256 File Encrypter (Chunks) =====")
    print("Made by José Castro")
    escolha = input("Choose (E = Encript / D = Decript): ").strip().upper()
    if escolha == "E":
        caminho = input("File directory to encript: ").strip()
        encrypt_file(caminho)
    elif escolha == "D":
        caminho = input("Choose the .enc file to decript: ").strip()
        codigo = input("code to decript: ").strip()
        decrypt_file(caminho, codigo)
    else:
        print(" Wrong choice! Press E ou D.")

if __name__ == "__main__":
    main()