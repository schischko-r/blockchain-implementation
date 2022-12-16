from Blockchain import Blockchain
import BeatyPrint

# Define users
users = [
    ('Alice', "Alice_public_key"),
    ('Bob', "Bob_public_key"),
    ('Charlie', "Charlie_public_key"),
    ('Diana', "Diana_public_key")
]


# Create blockchain
blockchain = Blockchain(users)
# Send money between users
blockchain.wallets[0].send_money(blockchain.wallets[1].public_key, 40)
