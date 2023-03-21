from Blockchain import Blockchain
from Wallet import Wallet


# Define users
users = [
    'Alice',
    'Bob',
    'Charlie',
    'Dave',
]

# Create blockchain
blockchain = Blockchain(users)

user_wallet = Wallet(blockchain)
