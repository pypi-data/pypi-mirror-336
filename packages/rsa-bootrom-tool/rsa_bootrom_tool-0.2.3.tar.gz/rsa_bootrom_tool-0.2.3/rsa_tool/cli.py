import argparse
import json
import binascii
import os
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


def rsa_sign_file(filepath, keyfile, out_file=None):
    key = load_key(keyfile, use_private=True)

    with open(filepath, "rb") as f:
        data = f.read()

    h = SHA256.new(data)
    digest = h.digest()
    signature = pkcs1_15.new(key).sign(h)

    print(f"SHA256 digest: {h.hexdigest()}")
    print(f"Signature (hex): {binascii.hexlify(signature).decode()}")

    if out_file:
        with open(out_file, "wb") as f:
            f.write(signature)
        print(f"Signature saved to: {out_file}")

        hash_file = os.path.splitext(out_file)[0] + ".hash"
        with open(hash_file, "wb") as f:
            f.write(digest)
        print(f"Hash saved to: {hash_file}")
    else:
        print("Error: please use -o to specify output signature file")


def export_c_header(keyfile, outfile, endian='little', fmt='uint8', hashfile=None, sigfile=None):
    with open(keyfile, "r") as f:
        key_data = json.load(f)

    n = int(key_data["n"], 16)
    e = int(key_data["e"], 16)

    n_len = (n.bit_length() + 7) // 8
    n_bytes = n.to_bytes(n_len, endian)
    e_bytes = e.to_bytes(4, endian)

    def format_array(name, data, fmt):
        lines = []
        if fmt == 'uint8':
            lines.append(f"static const uint8_t {name}[] = {{")
            for i in range(0, len(data), 8):
                chunk = ", ".join(f"0x{b:02X}" for b in data[i:i+8])
                lines.append(f"    {chunk},")
            lines.append("};\n")
        elif fmt == 'uint32':
            lines.append(f"static const uint32_t {name}[] = {{")
            for i in range(0, len(data), 4):
                chunk = data[i:i+4].ljust(4, b'\x00')
                val = int.from_bytes(chunk, endian)
                lines.append(f"    0x{val:08X},")
            lines.append("};\n")
        return "\n".join(lines)

    hash_bytes = None
    sig_bytes = None
    if hashfile:
        with open(hashfile, "rb") as f:
            hash_bytes = f.read()
    if sigfile:
        with open(sigfile, "rb") as f:
            sig_bytes = f.read()

    with open(outfile, "w") as f:
        f.write("#ifndef RSA_PUBKEY_H\n#define RSA_PUBKEY_H\n\n#include <stdint.h>\n\n")
        f.write(format_array("rsa_n", n_bytes, fmt))
        f.write(format_array("rsa_e", e_bytes, fmt))

        if hash_bytes:
            f.write(format_array("test_hash", hash_bytes, "uint8"))
        if sig_bytes:
            f.write(format_array("test_sig", sig_bytes, "uint8"))

        f.write("\n#endif // RSA_PUBKEY_H\n")

    print(f"Exported C header to: {outfile}")


def main():
    parser = argparse.ArgumentParser(description="RSA Tool for BootROM Secure Boot")
    subparsers = parser.add_subparsers(dest='command')

    parser_gen = subparsers.add_parser('genkey', help='Generate RSA key pair')
    parser_gen.add_argument('-o', '--out', default='rsa_key.json')
    parser_gen.add_argument('--keysize', type=int, default=2048)

    parser_sign_file = subparsers.add_parser('sign_file', help='Sign binary file and output .sig and .hash')
    parser_sign_file.add_argument('-k', '--key', required=True)
    parser_sign_file.add_argument('file')
    parser_sign_file.add_argument('-o', '--out', help='Output signature file')

    parser_export = subparsers.add_parser('export_c', help='Export C header')
    parser_export.add_argument('-k', '--key', required=True)
    parser_export.add_argument('-o', '--out', default='rsa_pubkey.h')
    parser_export.add_argument('--endian', choices=['little', 'big'], default='little')
    parser_export.add_argument('--format', choices=['uint8', 'uint32'], default='uint8')
    parser_export.add_argument('--hashfile', help='Optional SHA256 hash file')
    parser_export.add_argument('--sigfile', help='Optional RSA signature file')

    args = parser.parse_args()

    if args.command == 'genkey':
        generate_rsa_key(args.keysize, args.out)
    elif args.command == 'sign_file':
        rsa_sign_file(args.file, args.key, args.out)
    elif args.command == 'export_c':
        export_c_header(args.key, args.out, args.endian, args.format, args.hashfile, args.sigfile)
    else:
        parser.print_help()
