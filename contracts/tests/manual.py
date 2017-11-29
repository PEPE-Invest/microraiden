'''
Script for getting transaction arguments for manually testing the
RaidenMicroTransferChannels functions.
Not to be used in production.
Make sure you recheck the code for any changes, because we are not using
contract functions -> no need to run a chain.
You need to control both accounts and provide the private key & password.

E.g.
python -m tests.manual --sender 0x5601Ea8445A5d96EEeBF89A67C4199FbB7a43Fbb --receiver 0xc5075799C8d1e286bc7dC0f285668499DDB5286d --block 8888 --balance 10 --contract 0x1d579a9e095768b97e8532eaa470a3252cd5fae1 --sender-private-key 4f3edb4ed5b688f6e7bcecdd4cd3d3f247da580bee126d80c40e04764a632bf7 --receiver-private-key cd9edcab0a0434a0161b79c37b5fae85ae59f926e695da0184bf263509006f18 --sender-private-key-password-file --receiver-private-key-password-file

4f3edb4ed5b688f6e7bcecdd4cd3d3f247da580bee126d80c40e04764a632bf7
cd9edcab0a0434a0161b79c37b5fae85ae59f926e695da0184bf263509006f18

/Users/loredana/Library/Application\ Support/io.parity.ethereum/keys/kovan/UTC--2017-08-08T16-12-02Z--bb47507a-53cf-2e4b-68cc-0a6cfb352233
'''
import sys
import click
from utils import sign
from tests.utils import balance_proof_hash
from utils.utils import sol_sha3


@click.command()
@click.option(
    '--sender',
    help='Token sender.'
)
@click.option(
    '--receiver',
    help='Token receiver.'
)
@click.option(
    '--block',
    help='Block number at which the channel was created.'
)
@click.option(
    '--balance',
    help='Balance.'
)
@click.option(
    '--contract',
    help='RaidenMicroTransferChannels address.'
)
@click.option(
    '--sender-private-key',
    help="Private key for the sender's account."
)
@click.option(
    '--receiver-private-key',
    help="Private key for the receiver's account."
)
@click.option(
    '--sender-private-key-password-file',
    default=None,
    help='Path to file containing password for the JSON-encoded private key',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
@click.option(
    '--receiver-private-key-password-file',
    default=None,
    help='Path to file containing password for the JSON-encoded private key',
    type=click.Path(exists=True, dir_okay=False, resolve_path=True)
)
def main(**kwargs):
    sender = kwargs['sender']
    receiver = kwargs['receiver']
    balance = int(kwargs['balance'])
    block = int(kwargs['block'])
    contract = kwargs['contract']
    sender_private_key = kwargs['sender_private_key']
    receiver_private_key = kwargs['receiver_private_key']
    sender_private_key_password_file = kwargs['sender_private_key_password_file']
    receiver_private_key_password_file = kwargs['receiver_private_key_password_file']

    create_channel223_data = bytes.fromhex(receiver[2:].zfill(40))
    print('Create channel 223 data', create_channel223_data)

    if block is None:
        sys.exit(1)

    topup_channel223_data = receiver[2:].zfill(40) + hex(block)[2:].zfill(8)
    topup_channel223_data = bytes.fromhex(topup_channel223_data)
    print('Topup channel 223 data', topup_channel223_data)

    if contract is None:
        sys.exit(1)

    balance_message_hash = balance_proof_hash(receiver, block, balance, contract)
    print('Balance message hash', balance_message_hash)

    sender_private_key = sign.get_private_key(sender_private_key, sender_private_key_password_file)
    if sender_private_key is None:
        sys.exit(1)

    balance_message_signature, signer1 = sign.check(balance_message_hash, tester.k2)
    assert signer1 == sender
    print('Balance message signature', balance_message_signature)

    receiver_private_key = sign.get_private_key(receiver_private_key, receiver_private_key_password_file)
    if receiver_private_key is None:
        sys.exit(1)

    closing_signature, signer2 = sign.check(sol_sha3(balance_message_signature), tester.k3)
    assert signer1 == receiver
    print('Closing signature', closing_signature)


if __name__ == '__main__':
    main()
