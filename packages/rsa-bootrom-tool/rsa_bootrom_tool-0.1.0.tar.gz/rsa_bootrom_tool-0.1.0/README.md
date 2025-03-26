# RSA BootROM Secure Boot Tool

A command-line Python tool for generating RSA keys, signing and verifying messages or binary files (e.g., firmware), and exporting public keys to C header files for BootROM secure boot environments.

---

## ✅ Features

- Generate RSA key pairs (`n`, `e`, `d` in JSON)
- Sign a message or a SHA256 digest
- Sign binary files (firmware) by hashing with SHA256 and signing
- Verify signatures using message or binary file
- Export RSA public key (`n`, `e`) to C header file for BootROM integration
- Support for endian and array format selection in C export

---

## 📦 Dependencies

```bash
pip install pycryptodome
```

---

## 🛠 Usage

### 🔐 Generate RSA Key

```bash
python rsa_tool.py genkey -o rsa_key.json --keysize 1024
```

### ✍️ Sign Message (auto SHA256)

```bash
python rsa_tool.py sign -k rsa_key.json "bootloader image" -o signature.bin
```

### ✍️ Sign SHA256 Digest

```bash
python rsa_tool.py sign -k rsa_key.json --digest "AABBCCDDEEFF..." -o signature.bin
```

### ✅ Verify Message

```bash
python rsa_tool.py verify -k rsa_key.json "bootloader image" --sigfile signature.bin
```

### 🧾 Sign Binary File (e.g., firmware)

```bash
python rsa_tool.py sign_file -k rsa_key.json firmware.bin -o firmware.sig
```

### 🔍 Verify Binary File

```bash
python rsa_tool.py verify_file -k rsa_key.json firmware.bin --sigfile firmware.sig
```

### 📤 Export C Header (n, e)

```bash
python rsa_tool.py export_c -k rsa_key.json -o rsa_pubkey.h \
    --endian little --format uint32
```

---

## 📁 Example C Header Output

```c
#ifndef RSA_PUBKEY_H
#define RSA_PUBKEY_H

#include <stdint.h>

static const uint32_t rsa_n[] = {
    0xDEADBEEF, 0x12345678, ...
};

static const uint32_t rsa_e[] = {
    0x01000100,
};

#endif // RSA_PUBKEY_H
```

---

## 🧰 Author & License

MIT License. Created for BootROM secure boot flows using RSA signature with SHA256.

---

## 🔧 Roadmap Ideas

- Add support for `--hash` algorithm choice (SHA256, SHA384, etc.)
- Add PKCS#1 v2.1 (PSS) support
- Add structure export (e.g., TLV or CRC-appended formats)

---
