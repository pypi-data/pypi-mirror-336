import os
import json
import binascii
from rsa_tool import generate_rsa_key, load_key, rsa_sign, rsa_verify

def test_sign_and_verify_message(tmp_path):
    # Generate a temp key file
    key_file = tmp_path / "test_key.json"
    generate_rsa_key(key_size=1024, out_file=str(key_file))

    # Load keys
    priv_key = load_key(str(key_file), use_private=True)
    pub_key = load_key(str(key_file), use_private=False)

    # Message
    message = b"unit test message"

    # Sign
    h = __import__('Crypto.Hash.SHA256', fromlist=['SHA256']).SHA256.new(message)
    from Crypto.Signature import pkcs1_15
    signature = pkcs1_15.new(priv_key).sign(h)
    sig_hex = binascii.hexlify(signature).decode()

    # Verify
    assert rsa_verify(message, signature_hex=sig_hex, keyfile=str(key_file)) is None
