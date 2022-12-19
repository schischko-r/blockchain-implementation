from Blockchain import Blockchain
from Wallet import Wallet

from ECDSA import ecdsa
from ECDSA import elliptic_curves as ec

# Define users
users = [
    ('Alice', "Alice_public_key"),
    ('Bob', "Bob_public_key"),
    ('Charlie', "Charlie_public_key"),
    ('Diana', "Diana_public_key")
]


P = 233970423115425145524320034830162017933
G = ec.ECPoint(182, 85518893674295321206118380980485522083)
N = 29246302889428143187362802287225875743

curve = ec.EllipticCurve(-95051, 11279326, P)
dsa = ecdsa.EllipticCurveDSA(curve, G, N)

key = dsa.GeneratePair()
open_key = key[1]
closed_key = key[0]

sig = dsa.Sign(key, b'hello world')

if dsa.Verify(sig, key, b'hello world'):
    print('[**] Validation passed')
else:
    print('[!!] Validation failed.')

# Create blockchain
blockchain = Blockchain(users)

user_wallet = Wallet(blockchain)
