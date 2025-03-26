import argparse
import json
import binascii
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


def generate_rsa_key(key_size=2048, out_file="rsa_key.json"):
    key = RSA.generate(key_size)
    n = key.n
    e = key.e
    d = key.d

    key_data = {
        "n": hex(n),
        "e": hex(e),
        "d": hex(d)
    }

    with open(out_file, "w") as f:
        json.dump(key_data, f, indent=4)

    print(f"RSA key saved to {out_file} ({key_size}-bit, modulus length = {key_size // 8} bytes)")


def load_key(filename, use_private=True):
    with open(filename, "r") as f:
        key_data = json.load(f)
    n = int(key_data["n"], 16)
    e = int(key_data["e"], 16)
    d = int(key_data["d"], 16) if use_private and "d" in key_data else None

    if use_private and d:
        return RSA.construct((n, e, d))
    else:
        return RSA.construct((n, e))


def rsa_sign(message_or_digest, keyfile, is_digest=False, out_file=None):
    key = load_key(keyfile, use_private=True)

    if is_digest:
        try:
            hash_bytes = binascii.unhexlify(message_or_digest)
        except Exception:
            print("Error: Invalid hex digest.")
            return
        if len(hash_bytes) != 32:
            print("Error: SHA256 digest must be 64 hex characters (32 bytes)")
            return
        h = SHA256.new()
        h._digest = hash_bytes
    else:
        h = SHA256.new(message_or_digest)

    signature = pkcs1_15.new(key).sign(h)
    hex_sig = binascii.hexlify(signature).decode()
    print(f"Signature (hex): {hex_sig}")

    if out_file:
        with open(out_file, "wb") as f:
            f.write(signature)
        print(f"Signature saved to: {out_file}")


def rsa_verify(message, signature_hex=None, sigfile=None, keyfile=None):
    key = load_key(keyfile, use_private=False)
    h = SHA256.new(message)

    if sigfile:
        with open(sigfile, "rb") as f:
            signature = f.read()
    elif signature_hex:
        signature = binascii.unhexlify(signature_hex)
    else:
        print("Error: either --sigfile or signature hex must be provided.")
        return

    try:
        pkcs1_15.new(key).verify(h, signature)
        print("Signature is valid.")
    except Exception as e:
        print("Signature verification failed:", str(e))


def rsa_sign_file(filepath, keyfile, out_file=None):
    key = load_key(keyfile, use_private=True)

    with open(filepath, "rb") as f:
        data = f.read()

    h = SHA256.new(data)
    signature = pkcs1_15.new(key).sign(h)
    hex_sig = binascii.hexlify(signature).decode()

    print(f"Signature (hex): {hex_sig}")

    if out_file:
        with open(out_file, "wb") as f:
            f.write(signature)
        print(f"Signature saved to: {out_file}")


def rsa_verify_file(filepath, keyfile, signature_hex=None, sigfile=None):
    key = load_key(keyfile, use_private=False)

    with open(filepath, "rb") as f:
        data = f.read()

    h = SHA256.new(data)
    digest_hex = h.hexdigest()
    print(f"SHA256 digest: {digest_hex}")

    if sigfile:
        with open(sigfile, "rb") as f:
            signature = f.read()
    elif signature_hex:
        signature = binascii.unhexlify(signature_hex)
    else:
        print("Error: provide either signature hex or --sigfile")
        return

    try:
        pkcs1_15.new(key).verify(h, signature)
        print("Signature is valid.")
    except Exception as e:
        print("Signature verification failed:", str(e))


def export_c_header(keyfile, outfile, endian='little', fmt='uint8'):
    with open(keyfile, "r") as f:
        key_data = json.load(f)

    n_int = int(key_data["n"], 16)
    e_int = int(key_data["e"], 16)

    n_len = (n_int.bit_length() + 7) // 8
    n_bytes = n_int.to_bytes(n_len, byteorder=endian)
    e_bytes = e_int.to_bytes(4, byteorder=endian)

    def format_array(name, data, fmt):
        lines = []
        if fmt == 'uint8':
            lines.append(f"static const uint8_t {name}[] = {{")
            for i in range(0, len(data), 8):
                chunk = ", ".join(f"0x{b:02X}" for b in data[i:i+8])
                lines.append(f"    {chunk},")
            lines.append("};
")
        elif fmt == 'uint32':
            lines.append(f"static const uint32_t {name}[] = {{")
            for i in range(0, len(data), 4):
                chunk = data[i:i+4]
                if len(chunk) < 4:
                    chunk = chunk + b'\x00' * (4 - len(chunk))
                val = int.from_bytes(chunk, byteorder=endian)
                lines.append(f"    0x{val:08X},")
            lines.append("};
")
        return "\n".join(lines)

    with open(outfile, "w") as f:
        f.write("#ifndef RSA_PUBKEY_H\n#define RSA_PUBKEY_H\n\n")
        f.write("#include <stdint.h>\n\n")
        f.write(format_array("rsa_n", n_bytes, fmt))
        f.write(format_array("rsa_e", e_bytes, fmt))
        f.write("#endif // RSA_PUBKEY_H\n")

    print(f"Exported n and e to C header: {outfile} (byteorder = {endian}, format = {fmt})")


def main():
    parser = argparse.ArgumentParser(description="RSA Tool for BootROM Secure Boot")
    subparsers = parser.add_subparsers(dest='command')

    parser_gen = subparsers.add_parser('genkey', help='Generate RSA key pair')
    parser_gen.add_argument('-o', '--out', default='rsa_key.json', help='Output key file')
    parser_gen.add_argument('--keysize', type=int, default=2048, help='RSA key size (default: 2048)')

    parser_sign = subparsers.add_parser('sign', help='Sign a message or digest')
    parser_sign.add_argument('-k', '--key', required=True, help='Private key file (json)')
    parser_sign.add_argument('message', help='Message string or SHA256 hex digest')
    parser_sign.add_argument('--digest', action='store_true', help='Input is a SHA256 hex digest')
    parser_sign.add_argument('-o', '--out', help='Output binary signature file')

    parser_verify = subparsers.add_parser('verify', help='Verify a message signature')
    parser_verify.add_argument('-k', '--key', required=True, help='Public key file (json)')
    parser_verify.add_argument('message', help='Message string')
    parser_verify.add_argument('signature', nargs='?', help='Signature in hex (optional if --sigfile used)')
    parser_verify.add_argument('--sigfile', help='Signature binary file')

    parser_sign_file = subparsers.add_parser('sign_file', help='Sign a binary file')
    parser_sign_file.add_argument('-k', '--key', required=True, help='Private key file (json)')
    parser_sign_file.add_argument('file', help='Input binary file')
    parser_sign_file.add_argument('-o', '--out', help='Output binary signature file')

    parser_verify_file = subparsers.add_parser('verify_file', help='Verify a binary file')
    parser_verify_file.add_argument('-k', '--key', required=True, help='Public key file (json)')
    parser_verify_file.add_argument('file', help='Input binary file')
    parser_verify_file.add_argument('signature', nargs='?', help='Signature in hex (optional if --sigfile used)')
    parser_verify_file.add_argument('--sigfile', help='Signature binary file')

    parser_export = subparsers.add_parser('export_c', help='Export RSA n and e to C header file')
    parser_export.add_argument('-k', '--key', required=True, help='RSA key file (json)')
    parser_export.add_argument('-o', '--out', default='rsa_pubkey.h', help='Output header file')
    parser_export.add_argument('--endian', choices=['little', 'big'], default='little', help='Byte order')
    parser_export.add_argument('--format', choices=['uint8', 'uint32'], default='uint8', help='Array format')

    args = parser.parse_args()

    if args.command == 'genkey':
        generate_rsa_key(args.keysize, args.out)
    elif args.command == 'sign':
        rsa_sign(args.message if args.digest else args.message.encode(), args.key, is_digest=args.digest, out_file=args.out)
    elif args.command == 'verify':
        rsa_verify(args.message.encode(), signature_hex=args.signature, sigfile=args.sigfile, keyfile=args.key)
    elif args.command == 'sign_file':
        rsa_sign_file(args.file, args.key, out_file=args.out)
    elif args.command == 'verify_file':
        rsa_verify_file(filepath=args.file, keyfile=args.key, signature_hex=args.signature, sigfile=args.sigfile)
    elif args.command == 'export_c':
        export_c_header(args.key, args.out, args.endian, args.format)
    else:
        parser.print_help()
