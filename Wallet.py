import datetime


class Wallet:
    def __init__(self, public_name, public_key, blockchain):
        # Public name of the wallet
        self.public_name = public_name
        # Public key of the wallet
        self.public_key = public_key
        # Blockchain of the wallet
        self.blockchain = blockchain

    def get_balance(self):
        # Get balance of the wallet
        return sum([block.get_balance(self.public_key)
                    for block in self.blockchain.chain])

    def __str__(self):
        # Print wallet data to console
        return f'{self.public_name} balance: {self.get_balance()}'

    def send_money(self, recipient_public_key, value):
        # Send money to another wallet
        if self.get_balance() < value:
            # If the wallet doesn't have enough money
            print('Not enough money')
            return

        # Add block with sending money to another user to the blockchain
        self.blockchain.add_block(data=datetime.datetime.now(), sender_public_key=self.public_key,
                                  recipient_public_key=recipient_public_key, value=value)
