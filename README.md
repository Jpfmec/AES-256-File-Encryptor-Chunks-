# AES-256 File Encryptor (Chunks)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Size](https://img.shields.io/badge/File--Size-Large%20Files-blueviolet)

A **secure Python program** to encrypt and decrypt files of any size using **AES-256-GCM with chunked processing**, providing:

- Data confidentiality
- Integrity with authentication
- Support for large files (>GBs)
- Random secure code for decryption

---

##  Features

- Encrypt files of any size
- Decrypt files using the random code generated during encryption
- Chunked file processing to avoid memory overload
- Interactive menu with overwrite confirmation
- Secure implementation using:
  - AES-256-GCM (authenticated encryption)
  - PBKDF2-HMAC-SHA256 for key derivation
  - Random nonce and salt per file

---

##  Requirements

- Python 3.9 or higher
- `cryptography` library

Install dependencies:

```bash
pip install cryptography
