import os
import binascii
import bitcoin
from ethereum import utils
from secp256k1 import PrivateKey
from eth_utils import encode_hex
from utils.utils import sol_sha3


eth_prefix = "\x19Ethereum Signed Message:\n"


def eth_privtoaddr(priv) -> str:
    pub = bitcoin.encode_pubkey(bitcoin.privtopub(priv), 'bin_electrum')
    return "0x" + binascii.hexlify(sol_sha3(pub)[12:]).decode("ascii")


def eth_message_prefixed(msg: str) -> bytes:
    return eth_prefix + str(len(msg)) + msg


def eth_message_hex(msg: str) -> bytes:
    msg = eth_message_prefixed(msg)
    msg_hex = encode_hex(msg)
    return sol_sha3(msg_hex)


def eth_signed_typed_data_message(types, names, data) -> bytes:
    """
    types e.g. ('address', 'uint', ('uint', 32))
    names e.g. ('receiver', 'block_created', 'balance')
    data e.g. ('0x5601ea8445a5d96eeebf89a67c4199fbb7a43fbb', 3000, 1000)
    """
    assert len(types) == len(data) == len(names), 'Argument length mismatch.'

    sign_types = []
    sign_values = []
    for i, type in enumerate(types):
        if isinstance(type, tuple):
            sign_types.append(type[0] + str(type[1]))
            sign_values.append((data[i], type[1]))
        else:
            sign_types.append(type)
            sign_values.append(data[i])

        sign_types[i] += ' ' + names[i]

    return sol_sha3(sol_sha3(*sign_types), sol_sha3(*sign_values))


def sign(data: bytes, private_key_seed_ascii: str):
    priv = private_key_seed_ascii
    pk = PrivateKey(priv, raw=True)
    signature = pk.ecdsa_recoverable_serialize(pk.ecdsa_sign_recoverable(data, raw=True))
    signature = signature[0] + utils.bytearray_to_bytestr([signature[1]])
    return signature, eth_privtoaddr(priv)


def check(data: bytes, pk: bytes):
    return sign(data, pk)


def get_private_key(key_path, password_path=None):
    """Open a JSON-encoded private key and return it
    If a password file is provided, uses it to decrypt the key. If not, the
    password is asked interactively. Raw hex-encoded private keys are supported,
    but deprecated."""

    assert key_path, key_path
    if not os.path.exists(key_path):
        print("%s: no such file", key_path)
        return None

    if not check_permission_safety(key_path):
        print("Private key file %s must be readable only by its owner.", key_path)
        return None

    if password_path and not check_permission_safety(password_path):
        print("Password file %s must be readable only by its owner.", password_path)
        return None

    with open(key_path) as keyfile:
        private_key = keyfile.readline().strip()

        if is_hex(private_key) and len(decode_hex(private_key)) == 32:
            log.warning("Private key in raw format. Consider switching to JSON-encoded")
        else:
            keyfile.seek(0)
            try:
                json_data = json.load(keyfile)
                if password_path:
                    with open(password_path) as password_file:
                        password = password_file.readline().strip()
                else:
                    password = getpass.getpass("Enter the private key password: ")
                private_key = encode_hex(keys.decode_keystore_json(json_data, password))
            except ValueError:
                print("Invalid private key format or password!")
                return None

    return private_key
