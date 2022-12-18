import datetime
from Interface import InterfaceHandler
from ellipticcurve.privateKey import PrivateKey


class Wallet:

    def __init__(self, blockchain, public_name=None):
        # Blockchain of the wallet
        self.blockchain = blockchain
        self.interface = InterfaceHandler()
        if public_name is None:
            self.interface.new_user_welcoming_message(side_wallet=self)
        else:
            self.public_name = public_name
            # Public key of the wallet
            self.private_key = PrivateKey()
            self.public_key = self.private_key.publicKey()
            self.public_key_compressed = self.public_key.toCompressed()

    def get_balance(self):
        # Get balance of the wallet
        return sum([block.get_balance(self.public_key_compressed)
                    for block in self.blockchain.chain])

    def send_money(self, recipient_public_key, value):
        # Send money to another wallet
        if self.get_balance() < value:
            # If the wallet doesn't have enough money
            InterfaceHandler.Error('Not enough neurocoins')
            return

        # Add block with sending money to another user to the blockchain
        # find wallet with recipient public key
        self.blockchain.add_block(sender_wallet=self,
                                  recipient_wallet=self.blockchain.wallets[[wallet.public_key_compressed for wallet in self.blockchain.wallets].index(
                                      recipient_public_key)], value=value)

    # TODO: LOGIN TO THE WALLET
    def login(self, public_name):
        if public_name in [self.blockchain.wallets[i].public_name for i in range(len(self.blockchain.wallets))]:
            return True
        else:
            return False
