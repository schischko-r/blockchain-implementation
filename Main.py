from Blockchain import Blockchain
from Wallet import Wallet

# Define users
users = [
    ('Alice', "Alice_public_key"),
    ('Bob', "Bob_public_key"),
    ('Charlie', "Charlie_public_key"),
    ('Diana', "Diana_public_key")
]


# Create blockchain
blockchain = Blockchain(users)

user_wallet = Wallet(blockchain)
